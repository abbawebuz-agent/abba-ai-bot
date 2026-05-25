"""Database backup → Telegram private channel.

Usage:
    python manage.py backup_db                    # backup + upload
    python manage.py backup_db --no-upload        # only create local file
    python manage.py backup_db --keep-media       # also dump media/ files

Cron-friendly: writes status to stdout/stderr, exits non-zero on failure.

ENV variables required:
    DATABASE_URL                — auto (Railway provides)
    TELEGRAM_BOT_TOKEN          — auto (settings.TELEGRAM_BOT_TOKEN)
    BACKUP_CHANNEL_ID           — set this to your channel chat_id (-100...)
"""
import gzip
import json
import os
import subprocess
import tempfile
import time
import urllib.parse
from datetime import datetime
from urllib.parse import urlparse

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Backup PostgreSQL database (pg_dump → gzip) and upload to Telegram channel"

    def add_arguments(self, parser):
        parser.add_argument('--no-upload', action='store_true',
                            help="Skip Telegram upload (only create local .sql.gz)")
        parser.add_argument('--keep-media', action='store_true',
                            help="Also create media.tar.gz with uploaded files")
        parser.add_argument('--out', type=str, default=None,
                            help="Output directory (default: /tmp)")

    def handle(self, *args, **opts):
        token = getattr(settings, 'TELEGRAM_BOT_TOKEN', '') or os.environ.get('TELEGRAM_BOT_TOKEN', '')
        chat_id = (
            getattr(settings, 'BACKUP_CHANNEL_ID', '')
            or os.environ.get('BACKUP_CHANNEL_ID', '')
        )

        if not opts['no_upload']:
            if not token:
                raise CommandError("TELEGRAM_BOT_TOKEN sozlanmagan")
            if not chat_id:
                raise CommandError(
                    "BACKUP_CHANNEL_ID sozlanmagan. Railway Variables ga qo'shing.\n"
                    "Chat ID ni olish: kanaldan istalgan xabarni @userinfobot ga forward qiling."
                )

        db_url = self._get_db_url()
        ts = datetime.now().strftime('%Y%m%d_%H%M%S')
        out_dir = opts['out'] or tempfile.gettempdir()
        os.makedirs(out_dir, exist_ok=True)

        # 1. pg_dump
        dump_path = os.path.join(out_dir, f'jip_db_{ts}.sql.gz')
        self.stdout.write(f"📦 pg_dump → {dump_path}")
        size = self._pg_dump(db_url, dump_path)
        size_mb = size / (1024 * 1024)
        self.stdout.write(self.style.SUCCESS(f"   ✅ {size_mb:.2f} MB"))

        files_to_upload = [dump_path]

        # 2. Media archive (optional)
        if opts['keep_media']:
            media_root = getattr(settings, 'MEDIA_ROOT', None)
            if media_root and os.path.isdir(media_root):
                media_path = os.path.join(out_dir, f'jip_media_{ts}.tar.gz')
                self.stdout.write(f"📁 Media → {media_path}")
                msize = self._tar_media(media_root, media_path)
                self.stdout.write(self.style.SUCCESS(f"   ✅ {msize/(1024*1024):.2f} MB"))
                files_to_upload.append(media_path)

        # 3. Upload
        if not opts['no_upload']:
            self.stdout.write(f"📤 Upload → Telegram channel {chat_id}")
            for path in files_to_upload:
                caption = self._caption(path, ts)
                self._tg_upload(token, chat_id, path, caption)
                self.stdout.write(self.style.SUCCESS(f"   ✅ {os.path.basename(path)}"))
                time.sleep(1)  # Telegram rate-limit
            self.stdout.write(self.style.SUCCESS("\n🎉 Backup tugadi"))
        else:
            self.stdout.write(self.style.WARNING("\n⚠️  --no-upload — Telegram ga yuborilmadi"))

    # ──────────────────────────────────────────────────────────────────
    def _get_db_url(self):
        """Construct PostgreSQL connection URL from Django settings."""
        db = settings.DATABASES['default']
        if not db.get('HOST'):
            raise CommandError("DATABASE_URL/settings noto'g'ri")
        return {
            'host': db['HOST'],
            'port': str(db.get('PORT') or 5432),
            'user': db['USER'],
            'password': db['PASSWORD'],
            'name': db['NAME'],
        }

    def _pg_dump(self, db, out_path):
        """Run pg_dump and gzip output. Returns final size."""
        env = os.environ.copy()
        env['PGPASSWORD'] = db['password']
        cmd = [
            'pg_dump',
            '-h', db['host'],
            '-p', db['port'],
            '-U', db['user'],
            '-d', db['name'],
            '--no-owner',
            '--no-privileges',
            '--clean',
            '--if-exists',
        ]
        with gzip.open(out_path, 'wb', compresslevel=6) as gz:
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
            try:
                while True:
                    chunk = proc.stdout.read(65536)
                    if not chunk:
                        break
                    gz.write(chunk)
                proc.wait(timeout=600)
            except subprocess.TimeoutExpired:
                proc.kill()
                raise CommandError("pg_dump timeout (>10 daqiqa)")
            if proc.returncode != 0:
                err = proc.stderr.read().decode(errors='replace')
                raise CommandError(f"pg_dump xato (code {proc.returncode}):\n{err}")
        return os.path.getsize(out_path)

    def _tar_media(self, media_root, out_path):
        """tar+gzip media directory."""
        subprocess.run(
            ['tar', '-czf', out_path, '-C', os.path.dirname(media_root), os.path.basename(media_root)],
            check=True, capture_output=True,
        )
        return os.path.getsize(out_path)

    def _caption(self, path, ts):
        size_mb = os.path.getsize(path) / (1024 * 1024)
        kind = 'DB' if path.endswith('.sql.gz') else 'Media'
        return (
            f"🗄 <b>JIP {kind} Backup</b>\n"
            f"📅 {ts.replace('_', ' ')}\n"
            f"💾 {size_mb:.2f} MB\n"
            f"#backup #{kind.lower()}"
        )

    def _tg_upload(self, token, chat_id, file_path, caption):
        """Multipart upload to Telegram sendDocument."""
        import mimetypes
        import uuid
        url = f'https://api.telegram.org/bot{token}/sendDocument'
        boundary = uuid.uuid4().hex
        body = bytearray()

        def _field(name, value):
            body.extend(f'--{boundary}\r\n'.encode())
            body.extend(f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode())
            body.extend(str(value).encode())
            body.extend(b'\r\n')

        _field('chat_id', chat_id)
        _field('caption', caption)
        _field('parse_mode', 'HTML')

        # File part
        fname = os.path.basename(file_path)
        ctype = mimetypes.guess_type(fname)[0] or 'application/octet-stream'
        body.extend(f'--{boundary}\r\n'.encode())
        body.extend(f'Content-Disposition: form-data; name="document"; filename="{fname}"\r\n'.encode())
        body.extend(f'Content-Type: {ctype}\r\n\r\n'.encode())
        with open(file_path, 'rb') as f:
            body.extend(f.read())
        body.extend(b'\r\n')
        body.extend(f'--{boundary}--\r\n'.encode())

        import urllib.request
        req = urllib.request.Request(
            url, data=bytes(body),
            headers={'Content-Type': f'multipart/form-data; boundary={boundary}'},
        )
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                data = json.loads(resp.read())
                if not data.get('ok'):
                    raise CommandError(f"Telegram API xato: {data}")
        except urllib.error.HTTPError as e:
            body_err = e.read().decode(errors='replace')
            raise CommandError(f"Telegram HTTP {e.code}: {body_err}")
