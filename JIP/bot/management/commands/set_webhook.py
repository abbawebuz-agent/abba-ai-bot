"""
Telegram webhook URL ni o'rnatish.
"""
import asyncio

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Set or remove Telegram webhook URL'

    def add_arguments(self, parser):
        parser.add_argument('--url', help='Webhook URL (default: settings.TELEGRAM_WEBHOOK_URL)')
        parser.add_argument('--delete', action='store_true', help='Delete current webhook instead')

    def handle(self, *args, **options):
        from bot.bot import build_bot

        url = options['url'] or getattr(settings, 'TELEGRAM_WEBHOOK_URL', '')
        secret = getattr(settings, 'TELEGRAM_WEBHOOK_SECRET', '') or None

        async def _run():
            bot = build_bot()
            if options['delete']:
                await bot.delete_webhook(drop_pending_updates=True)
                self.stdout.write(self.style.SUCCESS('Webhook deleted'))
                return
            if not url:
                raise CommandError('TELEGRAM_WEBHOOK_URL not set')
            await bot.set_webhook(url=url, secret_token=secret, drop_pending_updates=True)
            self.stdout.write(self.style.SUCCESS(f'Webhook set: {url}'))

        asyncio.run(_run())
