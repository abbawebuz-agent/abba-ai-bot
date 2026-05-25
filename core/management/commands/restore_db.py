"""Restore database from a .sql.gz dump file.

Usage:
    python manage.py restore_db /path/to/jip_db_20260525_040000.sql.gz
    python manage.py restore_db /tmp/dump.sql.gz --yes

⚠️  Destructive! Production data overwrites.
"""
import gzip
import os
import subprocess

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Restore PostgreSQL database from a .sql.gz dump"

    def add_arguments(self, parser):
        parser.add_argument('dump_path', type=str, help='Path to .sql.gz dump file')
        parser.add_argument('--yes', action='store_true',
                            help="Tasdiqlash so'rovini o'tkazib yuboring (destructive!)")

    def handle(self, *args, **opts):
        path = opts['dump_path']
        if not os.path.isfile(path):
            raise CommandError(f"Fayl topilmadi: {path}")

        db = settings.DATABASES['default']
        size_mb = os.path.getsize(path) / (1024 * 1024)

        self.stdout.write(self.style.WARNING(
            f"\n⚠️  DESTRUCTIVE OPERATION ⚠️\n"
            f"Database: {db['NAME']} @ {db['HOST']}\n"
            f"Dump fayl: {path} ({size_mb:.2f} MB)\n"
            f"Bu joriy datani O'CHIRADI va dumpdan tiklaydi.\n"
        ))

        if not opts['yes']:
            confirm = input("'YES' deb yozing davom etish uchun: ")
            if confirm.strip() != 'YES':
                self.stdout.write(self.style.ERROR("Bekor qilindi"))
                return

        env = os.environ.copy()
        env['PGPASSWORD'] = db['PASSWORD']

        psql_cmd = [
            'psql',
            '-h', db['HOST'],
            '-p', str(db.get('PORT') or 5432),
            '-U', db['USER'],
            '-d', db['NAME'],
            '--single-transaction',
            '--set', 'ON_ERROR_STOP=on',
        ]

        self.stdout.write(f"📥 Restore boshlanmoqda...")
        with gzip.open(path, 'rb') as gz:
            proc = subprocess.Popen(psql_cmd, stdin=subprocess.PIPE,
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
            try:
                stdout, stderr = proc.communicate(input=gz.read(), timeout=600)
            except subprocess.TimeoutExpired:
                proc.kill()
                raise CommandError("psql restore timeout (>10 daqiqa)")

            if proc.returncode != 0:
                raise CommandError(
                    f"psql xato (code {proc.returncode}):\n"
                    f"STDOUT:\n{stdout.decode(errors='replace')[:2000]}\n"
                    f"STDERR:\n{stderr.decode(errors='replace')[:2000]}"
                )

        self.stdout.write(self.style.SUCCESS("✅ Restore muvaffaqiyatli tugadi!"))
        self.stdout.write(self.style.WARNING(
            "ℹ️  Eslatma: media fayllar alohida tiklanishi kerak (agar backup ichida bo'lsa)"
        ))
