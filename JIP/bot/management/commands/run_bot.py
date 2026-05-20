"""
Long-polling rejimida botni ishga tushirish (dev uchun).
"""
import asyncio

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Run the JIP Telegram bot in polling mode (development)'

    def handle(self, *args, **options):
        from bot.bot import build_bot, build_dispatcher

        async def _run():
            bot = build_bot()
            dp = build_dispatcher()
            await bot.delete_webhook(drop_pending_updates=True)
            self.stdout.write(self.style.SUCCESS('Bot started — polling…'))
            await dp.start_polling(bot)

        asyncio.run(_run())
