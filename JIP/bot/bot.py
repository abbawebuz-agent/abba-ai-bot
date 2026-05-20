"""
JIP Telegram bot — aiogram 3 setup.
"""
from __future__ import annotations

import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from django.conf import settings

logger = logging.getLogger(__name__)


def build_bot() -> Bot:
    token = settings.TELEGRAM_BOT_TOKEN
    if not token:
        raise RuntimeError('TELEGRAM_BOT_TOKEN .env da belgilanmagan')
    return Bot(token=token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


def build_dispatcher() -> Dispatcher:
    from bot.handlers.registration import router as registration_router
    from bot.handlers.language import router as language_router
    from bot.handlers.menu import router as menu_router
    from bot.handlers.promo import router as promo_router

    dp = Dispatcher(storage=MemoryStorage())
    # Tartib muhim — promo router har qanday matnli xabarni tutadi,
    # shuning uchun u eng oxirida.
    dp.include_router(registration_router)
    dp.include_router(language_router)
    dp.include_router(menu_router)
    dp.include_router(promo_router)
    return dp
