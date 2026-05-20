"""
Promo kod (skretch karta) skanlash — har matnli xabar promo kod sifatida tekshiriladi.

Bu handler eng oxirda chaqiriladi (boshqa handler'lar ushlamaganda).
"""
from __future__ import annotations

import re

from aiogram import F, Router
from aiogram.types import Message

from bot import services
from bot.handlers.registration import _send_scan_result
from bot.translations import t
from core.models import TelegramUser

router = Router(name='promo')

# Skretch kartadagi kod: 4-32 alfa-raqam (kichik/katta harf)
PROMO_CODE_RE = re.compile(r'^[A-Za-z0-9]{4,32}$')


@router.message(F.text)
async def maybe_promo_code(message: Message) -> None:
    raw = (message.text or '').strip()
    if not PROMO_CODE_RE.match(raw):
        return

    user = await services.get_user_by_telegram_id(message.from_user.id)
    if user is None or not user.user_type:
        return
    lang = user.language or 'uz_latin'

    if user.user_type != TelegramUser.USER_TYPE_SANTENIK:
        await message.answer(t(lang, 'promo_wrong_role'))
        return

    result = await services.scan_qr_code(user.pk, raw, source='bot')
    await _send_scan_result(message, lang, result)
