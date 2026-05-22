"""Telegram webhook URL ni Railway domeniga o'rnatish."""
import asyncio
import logging
from django.core.management.base import BaseCommand
from django.conf import settings

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Telegram botni webhook rejimiga o\'tkazish'

    def handle(self, *args, **options):
        webhook_url = getattr(settings, 'WEBHOOK_URL', '')
        token = getattr(settings, 'TELEGRAM_BOT_TOKEN', '')

        if not token:
            self.stderr.write('TELEGRAM_BOT_TOKEN o\'rnatilmagan — o\'tkazildi')
            return

        if not webhook_url:
            self.stderr.write('WEBHOOK_URL o\'rnatilmagan — o\'tkazildi')
            return

        desired = f"{webhook_url.rstrip('/')}/webhook/{token}"

        async def _set():
            from bot.bot import bot
            try:
                info = await bot.get_webhook_info()
                if info and info.url == desired:
                    self.stdout.write(f'Webhook allaqachon o\'rnatilgan: {desired}')
                    return
                await bot.set_webhook(
                    url=desired,
                    allowed_updates=['message', 'callback_query'],
                    drop_pending_updates=False,
                )
                self.stdout.write(self.style.SUCCESS(f'Webhook o\'rnatildi: {desired}'))
            except Exception as e:
                self.stderr.write(f'Webhook xatolik: {e}')
            finally:
                await bot.session.close()

        asyncio.run(_set())
