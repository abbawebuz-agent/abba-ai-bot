"""Telegram bot orqali so'nggi updatelarni o'qib, kanal/chat ID larini ko'rsatadi.

Usage:
    1. Botni kanalga ADMIN qilib qo'shing
    2. Kanalda biror xabar yuboring (yoki "test" so'zi)
    3. Bu komandani ishga tushiring:

       python manage.py get_chat_id

    Natija: ID, nom va turi (channel/group/private chat) ko'rsatiladi.
"""
import json
import urllib.request

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Telegram bot so'nggi updatelaridagi chat ID larini ko'rsatadi"

    def handle(self, *args, **opts):
        token = getattr(settings, 'TELEGRAM_BOT_TOKEN', '')
        if not token:
            raise CommandError("TELEGRAM_BOT_TOKEN sozlanmagan")

        # Get last 100 updates
        url = f'https://api.telegram.org/bot{token}/getUpdates?limit=100'
        try:
            with urllib.request.urlopen(url, timeout=10) as r:
                data = json.loads(r.read())
        except Exception as exc:
            raise CommandError(f"Telegram API xato: {exc}")

        if not data.get('ok'):
            raise CommandError(f"API javobi xato: {data}")

        updates = data.get('result', [])
        if not updates:
            self.stdout.write(self.style.WARNING(
                "⚠️  So'nggi updatelar yo'q.\n"
                "Botni kanalga admin qiling va kanalda biror xabar yuboring,\n"
                "keyin bu buyruqni qayta ishga tushiring.\n\n"
                "Eslatma: agar bot webhook'da ishlasa, getUpdates ishlamaydi.\n"
                "Bu holatda @userinfobot dan foydalaning."
            ))
            return

        seen = {}
        for upd in updates:
            for key in ('channel_post', 'message', 'edited_channel_post', 'edited_message'):
                msg = upd.get(key)
                if not msg:
                    continue
                chat = msg.get('chat', {})
                cid = chat.get('id')
                if cid in seen:
                    continue
                seen[cid] = {
                    'id': cid,
                    'type': chat.get('type'),
                    'title': chat.get('title') or chat.get('username') or chat.get('first_name', '—'),
                    'username': chat.get('username'),
                }

        if not seen:
            self.stdout.write(self.style.WARNING("Update bor lekin chat info yo'q"))
            return

        self.stdout.write(self.style.SUCCESS(f"\n📋 Topilgan {len(seen)} ta chat:\n"))
        for c in seen.values():
            self.stdout.write(f"  ID: {self.style.SUCCESS(str(c['id']))}")
            self.stdout.write(f"  Turi: {c['type']}")
            self.stdout.write(f"  Nomi: {c['title']}")
            if c['username']:
                self.stdout.write(f"  Username: @{c['username']}")
            self.stdout.write("")

        self.stdout.write(self.style.SUCCESS(
            "✅ Backup kanali uchun 'channel' turidagi ID ni oling (odatda -100... bilan boshlanadi)\n"
            "Va Railway Variables ga BACKUP_CHANNEL_ID sifatida qo'shing."
        ))
