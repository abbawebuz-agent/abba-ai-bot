"""Test Telegram backup channel connection.

Sends a small test message to BACKUP_CHANNEL_ID. Useful to verify:
  - token is correct
  - chat_id is correct
  - bot is admin of the channel with "Post Messages" permission

Usage:
    python manage.py test_backup_channel
"""
import json
import os
import urllib.parse
import urllib.request

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "BACKUP_CHANNEL_ID kanaliga test xabar yuboradi"

    def handle(self, *args, **opts):
        token = getattr(settings, 'TELEGRAM_BOT_TOKEN', '')
        chat_id = (
            getattr(settings, 'BACKUP_CHANNEL_ID', '')
            or os.environ.get('BACKUP_CHANNEL_ID', '')
        )

        self.stdout.write(f"\n🔧 Sozlamalar:")
        self.stdout.write(f"   TELEGRAM_BOT_TOKEN: {'✅ bor' if token else '❌ yo''q'}")
        self.stdout.write(f"   BACKUP_CHANNEL_ID:  {chat_id or '❌ yo''q'}\n")

        if not token:
            raise CommandError("TELEGRAM_BOT_TOKEN sozlanmagan")
        if not chat_id:
            raise CommandError("BACKUP_CHANNEL_ID sozlanmagan")

        # 1. getMe — bot info
        self.stdout.write("🤖 Bot ma'lumotlari:")
        try:
            with urllib.request.urlopen(f'https://api.telegram.org/bot{token}/getMe', timeout=10) as r:
                me = json.loads(r.read())
                if me.get('ok'):
                    info = me['result']
                    self.stdout.write(
                        f"   ✅ @{info.get('username')} ({info.get('first_name')}) ID={info.get('id')}"
                    )
                else:
                    raise CommandError(f"getMe javobi xato: {me}")
        except Exception as exc:
            raise CommandError(f"getMe HTTP xato: {exc}")

        # 2. getChat — channel info
        self.stdout.write(f"\n📺 Kanal ma'lumotlari (chat_id={chat_id}):")
        try:
            url = f'https://api.telegram.org/bot{token}/getChat?chat_id={urllib.parse.quote(str(chat_id))}'
            with urllib.request.urlopen(url, timeout=10) as r:
                chat = json.loads(r.read())
                if chat.get('ok'):
                    info = chat['result']
                    self.stdout.write(self.style.SUCCESS(
                        f"   ✅ Turi:  {info.get('type')}\n"
                        f"   ✅ Nomi:  {info.get('title') or info.get('first_name')}\n"
                        f"   ✅ ID:    {info.get('id')}"
                    ))
                else:
                    raise CommandError(f"getChat javobi xato: {chat}")
        except urllib.error.HTTPError as e:
            body = e.read().decode(errors='replace')
            raise CommandError(
                f"getChat HTTP {e.code}: {body}\n\n"
                f"Mumkin sabablar:\n"
                f"  - Chat ID noto'g'ri (try -100... bilan boshlash kerak channel uchun)\n"
                f"  - Bot kanalga admin emas\n"
                f"  - Bot bloklangan"
            )

        # 3. sendMessage — test message
        self.stdout.write(f"\n📤 Test xabar yuborilmoqda...")
        try:
            url = f'https://api.telegram.org/bot{token}/sendMessage'
            data = urllib.parse.urlencode({
                'chat_id': chat_id,
                'text': (
                    '🧪 <b>Test xabar</b>\n\n'
                    "Backup tizimi ulanish testi muvaffaqiyatli.\n"
                    'Endi <code>python manage.py backup_db</code> '
                    'yoki admin panel tugmasini ishlatishingiz mumkin.\n\n'
                    '#test #backup'
                ),
                'parse_mode': 'HTML',
            }).encode()
            req = urllib.request.Request(url, data=data)
            with urllib.request.urlopen(req, timeout=10) as r:
                resp = json.loads(r.read())
                if resp.get('ok'):
                    self.stdout.write(self.style.SUCCESS(
                        f"\n🎉 Hammasi tayyor! Test xabar kanalga yuborildi.\n"
                        f"   Message ID: {resp['result'].get('message_id')}\n\n"
                        f"Endi backup ishlaydi. Admin paneldan tugmani bosishingiz mumkin."
                    ))
                else:
                    raise CommandError(f"sendMessage javobi xato: {resp}")
        except urllib.error.HTTPError as e:
            body = e.read().decode(errors='replace')
            raise CommandError(
                f"sendMessage HTTP {e.code}: {body}\n\n"
                f"Mumkin sabablar:\n"
                f"  - Bot 'Post Messages' ruxsatiga ega emas\n"
                f"  - Kanal turi (forum/comments) sendMessage qabul qilmaydi"
            )
