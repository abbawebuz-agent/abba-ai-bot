#!/usr/bin/env python
"""Local polling mode — Railway webhook olmay turib botni test qilish.
Ishlatish: TELEGRAM_BOT_TOKEN=xxx python run_polling.py
       yoki: python run_polling.py <BOT_TOKEN>
"""
import os
import sys
import asyncio
import django
import logging

# Token olish
token = os.environ.get('TELEGRAM_BOT_TOKEN', '')
if not token and len(sys.argv) > 1:
    token = sys.argv[1]

if not token:
    print("XATO: Token kerak!")
    print("  python run_polling.py <BOT_TOKEN>")
    print("  yoki: TELEGRAM_BOT_TOKEN=xxx python run_polling.py")
    sys.exit(1)

os.environ['TELEGRAM_BOT_TOKEN'] = token
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mona.settings.base')
os.environ.setdefault('SECRET_KEY', 'local-dev-secret-key-only')
os.environ.setdefault('DEBUG', 'True')

django.setup()

from django.conf import settings
settings.TELEGRAM_BOT_TOKEN = token

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
)
logger = logging.getLogger(__name__)


async def main():
    # bot.py dan barcha handler lar ro'yxatdan o'tgan dp va bot ni olish
    from bot.bot import bot, dp

    if bot is None:
        logger.error("Bot None — token noto'g'ri yoki bot.py da xatolik")
        return

    # Eski webhookni o'chirish (agar railway da o'rnatilgan bo'lsa)
    await bot.delete_webhook(drop_pending_updates=True)

    me = await bot.get_me()
    logger.info(f"Bot ishga tushdi: @{me.username} — {me.full_name}")
    logger.info("Polling... To'xtatish: Ctrl+C")

    try:
        await dp.start_polling(bot, allowed_updates=['message', 'callback_query'])
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(main())
