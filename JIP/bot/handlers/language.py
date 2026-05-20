"""
Menyu orqali tilni o'zgartirish.
"""
from __future__ import annotations

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from django.conf import settings

from bot import keyboards as kb
from bot import services
from bot.translations import t
from core.models import TelegramUser

router = Router(name='language')


@router.callback_query(F.data.startswith('lang:'))
async def on_language_switch(cq: CallbackQuery, state: FSMContext) -> None:
    """Tilni menyudan keyin almashtirish (FSM tashqarisida ham ishlaydi)."""
    fsm_state = await state.get_state()
    if fsm_state is not None:
        # Registration FSM ichidagi callback bo'lsa o'tkazib yuboramiz
        return

    lang = cq.data.split(':', 1)[1]
    if lang not in ('uz_latin', 'ru'):
        await cq.answer()
        return

    user = await services.get_user_by_telegram_id(cq.from_user.id)
    if user is None:
        await cq.answer()
        return

    await services.update_user_fields(user.pk, language=lang)
    await cq.message.edit_text(t(lang, 'language_changed'))

    web_app_url = getattr(settings, 'WEB_APP_URL', '') or None
    if user.user_type == TelegramUser.USER_TYPE_SOTUVCHI:
        markup = kb.kb_seller_menu(lang, web_app_url=web_app_url)
    else:
        markup = kb.kb_santenik_menu(lang, web_app_url=web_app_url)
    await cq.message.answer(t(lang, 'registration_complete'), reply_markup=markup)
    await cq.answer()
