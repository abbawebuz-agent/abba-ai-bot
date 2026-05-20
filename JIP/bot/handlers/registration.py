"""
Registration FSM handlers — TZ §6.2.
"""
from __future__ import annotations

from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from django.conf import settings

from bot import keyboards as kb
from bot import services
from bot.states import RegistrationStates
from bot.translations import t
from core.models import TelegramUser

router = Router(name='registration')


async def _get_lang(state: FSMContext, default: str = 'uz_latin') -> str:
    data = await state.get_data()
    return data.get('language', default)


@router.message(CommandStart(deep_link=True))
async def start_with_deeplink(message: Message, state: FSMContext, command) -> None:
    """`/start <hash>` — deep link to scan QR via hash_code."""
    payload = (command.args or '').strip()
    if not payload:
        await start(message, state)
        return

    user = await services.get_user_by_telegram_id(message.from_user.id)
    if not user or not user.user_type:
        await state.update_data(pending_promo_code=payload)
        await start(message, state)
        return

    lang = user.language or 'uz_latin'
    result = await services.scan_qr_code(user.pk, payload, source='bot')
    await _send_scan_result(message, lang, result)


@router.message(CommandStart())
async def start(message: Message, state: FSMContext) -> None:
    user = await services.get_user_by_telegram_id(message.from_user.id)
    if user and user.user_type:
        await _show_main_menu(message, user)
        return

    await state.clear()
    await message.answer(t('uz_latin', 'choose_language'), reply_markup=kb.kb_language())
    await state.set_state(RegistrationStates.waiting_for_language)


@router.callback_query(RegistrationStates.waiting_for_language, F.data.startswith('lang:'))
async def on_language_chosen(cq: CallbackQuery, state: FSMContext) -> None:
    lang = cq.data.split(':', 1)[1]
    if lang not in ('uz_latin', 'ru'):
        await cq.answer()
        return
    await state.update_data(language=lang)
    await cq.message.edit_text(t(lang, 'lang_chosen'))
    await cq.message.answer(t(lang, 'welcome'))
    await cq.message.answer(t(lang, 'ask_name'))
    await state.set_state(RegistrationStates.waiting_for_name)
    await cq.answer()


@router.message(RegistrationStates.waiting_for_name, F.text)
async def on_name(message: Message, state: FSMContext) -> None:
    name = (message.text or '').strip()
    if len(name) < 2:
        lang = await _get_lang(state)
        await message.answer(t(lang, 'ask_name'))
        return
    await state.update_data(name=name)
    lang = await _get_lang(state)
    await message.answer(t(lang, 'ask_user_type'), reply_markup=kb.kb_user_type(lang))
    await state.set_state(RegistrationStates.waiting_for_user_type)


@router.callback_query(RegistrationStates.waiting_for_user_type, F.data.startswith('role:'))
async def on_role(cq: CallbackQuery, state: FSMContext) -> None:
    role = cq.data.split(':', 1)[1]
    if role not in ('santenik', 'sotuvchi'):
        await cq.answer()
        return
    await state.update_data(user_type=role)
    lang = await _get_lang(state)
    await cq.message.edit_reply_markup(reply_markup=None)
    await cq.message.answer(t(lang, 'ask_privacy'), reply_markup=kb.kb_privacy(lang))
    await state.set_state(RegistrationStates.waiting_for_privacy)
    await cq.answer()


@router.callback_query(RegistrationStates.waiting_for_privacy, F.data.startswith('privacy:'))
async def on_privacy(cq: CallbackQuery, state: FSMContext) -> None:
    decision = cq.data.split(':', 1)[1]
    lang = await _get_lang(state)
    if decision != 'agree':
        await cq.message.edit_text(t(lang, 'privacy_required'))
        await state.clear()
        await cq.answer()
        return
    await state.update_data(privacy_accepted=True)
    await cq.message.edit_reply_markup(reply_markup=None)
    await cq.message.answer(t(lang, 'ask_phone'), reply_markup=kb.kb_phone(lang))
    await state.set_state(RegistrationStates.waiting_for_phone)
    await cq.answer()


@router.message(RegistrationStates.waiting_for_phone, F.contact)
async def on_phone(message: Message, state: FSMContext) -> None:
    phone = (message.contact.phone_number or '').strip()
    await state.update_data(phone_number=phone)
    lang = await _get_lang(state)
    await message.answer(t(lang, 'ask_location'), reply_markup=kb.kb_location(lang))
    await state.set_state(RegistrationStates.waiting_for_location)


@router.message(RegistrationStates.waiting_for_location, F.location)
async def on_location(message: Message, state: FSMContext) -> None:
    lat, lon = message.location.latitude, message.location.longitude
    await state.update_data(latitude=lat, longitude=lon)
    await _finalise_registration(message, state)


@router.message(RegistrationStates.waiting_for_location, F.text)
async def on_location_skip(message: Message, state: FSMContext) -> None:
    """Manual lokatsiya keyin — hozircha skip."""
    await _finalise_registration(message, state)


async def _finalise_registration(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    lang = data.get('language', 'uz_latin')
    name = (data.get('name') or '').strip()
    first_name, _, last_name = name.partition(' ')

    user, created = await services.get_or_create_user(
        telegram_id=message.from_user.id,
        defaults={
            'username': message.from_user.username,
            'first_name': first_name or message.from_user.first_name,
            'last_name': last_name or message.from_user.last_name,
            'language': lang,
        },
    )
    await services.update_user_fields(
        user.pk,
        username=message.from_user.username,
        first_name=first_name or message.from_user.first_name,
        last_name=last_name or message.from_user.last_name,
        language=lang,
        phone_number=data.get('phone_number'),
        latitude=data.get('latitude'),
        longitude=data.get('longitude'),
        user_type=data.get('user_type'),
        privacy_accepted=bool(data.get('privacy_accepted')),
    )

    # Sotuvchi do'kon biriktirilishini tekshiradi
    if data.get('user_type') == TelegramUser.USER_TYPE_SOTUVCHI:
        store = await services.find_store_for_seller(data.get('phone_number') or '', user.pk)
        if store is None:
            support = services.support_contact()
            await message.answer(
                t(lang, 'store_not_found', support=support),
                reply_markup=kb.kb_remove(),
            )
            await state.clear()
            return
        await state.update_data(store_id=store.pk, store_name=store.name)
        await message.answer(
            t(lang, 'store_found', store=store.name),
            reply_markup=kb.kb_yes_no(lang, 'store_confirm'),
        )
        await state.set_state(RegistrationStates.waiting_for_store_confirmation)
        return

    # Santenik darhol menyuga
    fresh_user = await services.get_user_by_telegram_id(message.from_user.id)
    await _show_main_menu(message, fresh_user)
    await state.clear()


@router.callback_query(RegistrationStates.waiting_for_store_confirmation, F.data.startswith('store_confirm:'))
async def on_store_confirm(cq: CallbackQuery, state: FSMContext) -> None:
    decision = cq.data.split(':', 1)[1]
    data = await state.get_data()
    lang = data.get('language', 'uz_latin')

    if decision != 'yes':
        await cq.message.edit_text(t(lang, 'wait_admin_link_seller', support=services.support_contact()))
        await state.clear()
        await cq.answer()
        return

    await cq.message.edit_reply_markup(reply_markup=None)
    user = await services.get_user_by_telegram_id(cq.from_user.id)
    await _show_main_menu(cq.message, user)
    await state.clear()
    await cq.answer()


async def _show_main_menu(message: Message, user: TelegramUser) -> None:
    lang = (user.language if user else None) or 'uz_latin'
    web_app_url = getattr(settings, 'WEB_APP_URL', '') or None
    if user and user.user_type == TelegramUser.USER_TYPE_SOTUVCHI:
        markup = kb.kb_seller_menu(lang, web_app_url=web_app_url)
    else:
        markup = kb.kb_santenik_menu(lang, web_app_url=web_app_url)
    await message.answer(t(lang, 'registration_complete'), reply_markup=markup)


async def _send_scan_result(message: Message, lang: str, result) -> None:
    """Scan natijasini foydalanuvchiga ko'rsatish."""
    if result.status == 'success':
        await message.answer(t(
            lang, 'promo_success',
            points=result.points, store=result.store_name, balance=result.balance,
        ))
    elif result.status == 'invalid':
        await message.answer(t(lang, 'promo_invalid'))
    elif result.status == 'used':
        await message.answer(t(lang, 'promo_used'))
    elif result.status == 'blocked':
        until = result.blocked_until.strftime('%Y-%m-%d %H:%M') if result.blocked_until else ''
        await message.answer(t(lang, 'promo_blocked', until=until))
    elif result.status == 'wrong_role':
        await message.answer(t(lang, 'promo_wrong_role'))
    else:
        await message.answer(t(lang, 'error_generic'))
