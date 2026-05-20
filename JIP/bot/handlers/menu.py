"""
Asosiy menyu handler'lari — ham santenik, ham sotuvchi uchun.
"""
from __future__ import annotations

from aiogram import F, Router
from aiogram.types import Message

from bot import keyboards as kb
from bot import services
from bot.translations import TRANSLATIONS, t
from core.models import TelegramUser

router = Router(name='menu')


def _build_menu_keys() -> dict[str, str]:
    """Tarjima qilingan tugma matnlari → ichki action kaliti."""
    keys = {}
    for lang_pack in TRANSLATIONS.values():
        keys[lang_pack['menu_balance']] = 'balance'
        keys[lang_pack['menu_my_balance']] = 'balance'
        keys[lang_pack['menu_gifts']] = 'gifts'
        keys[lang_pack['menu_orders']] = 'orders'
        keys[lang_pack['menu_top_month']] = 'top_month'
        keys[lang_pack['menu_top_all']] = 'top_all'
        keys[lang_pack['menu_video']] = 'video'
        keys[lang_pack['menu_language']] = 'language'
        keys[lang_pack['menu_help']] = 'help'
        keys[lang_pack['menu_sales_history']] = 'sales_history'
        keys[lang_pack['menu_my_store']] = 'my_store'
        keys[lang_pack['menu_admin_contact']] = 'admin_contact'
    return keys


MENU_KEYS = _build_menu_keys()


@router.message(F.text.in_(MENU_KEYS.keys()))
async def on_menu_press(message: Message) -> None:
    action = MENU_KEYS[message.text]
    user = await services.get_user_by_telegram_id(message.from_user.id)
    if user is None or not user.user_type:
        return
    lang = user.language or 'uz_latin'

    if action == 'balance':
        balance = await services.get_user_balance(user.pk)
        await message.answer(t(lang, 'balance_info', balance=balance))

    elif action == 'help':
        await message.answer(t(lang, 'help_text', support=services.support_contact()))

    elif action == 'admin_contact':
        await message.answer(services.support_contact())

    elif action == 'language':
        await message.answer(t(lang, 'choose_language'), reply_markup=kb.kb_language())

    else:
        # Qolgan menyular — Web App ichida ko'rsatiladi
        await message.answer(t(lang, 'no_data'))
