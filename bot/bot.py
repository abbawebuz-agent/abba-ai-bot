"""
Telegram bot implementation using aiogram.
"""
import asyncio
import logging
import os
from types import SimpleNamespace
import django
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery, Update
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import BaseMiddleware
from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError
from aiogram.filters import ExceptionTypeFilter
from aiogram.types import ErrorEvent
from asgiref.sync import sync_to_async
from django.conf import settings
from django.db import transaction
from django.utils import timezone
from core.models import TelegramUser, QRCode, QRCodeScanAttempt, Gift, GiftRedemption, VideoInstruction, UzRegion, UzDistrict
from core.utils import generate_qr_code_image
from core.regions import UZBEKISTAN_REGIONS
from .translations import get_text, TRANSLATIONS
from .location_picker import (
    build_region_keyboard,
    build_district_keyboard,
    find_district_data,
    CALLBACK_REGION_PREFIX,
    CALLBACK_DISTRICT_PREFIX,
    CALLBACK_BACK as CALLBACK_SETLOC_BACK,
)

# Настройка Django для использования в боте
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mona.settings')
django.setup()

logger = logging.getLogger(__name__)


async def _safe_delete_message(message: Message) -> None:
    """Удаляет сообщение; при ожидаемых ошибках Telegram (can't delete / not found) — тихо игнорируем."""
    try:
        await message.delete()
    except TelegramBadRequest as e:
        msg = str(e).lower()
        if "can't be deleted for everyone" in msg or "message to delete not found" in msg:
            logger.debug("Message delete skipped: %s", e)
        else:
            raise

# ── Sentry для бота ──────────────────────────────────────────────────────────
_sentry_dsn = getattr(settings, 'SENTRY_DSN', '') or os.environ.get('SENTRY_DSN', '')
if _sentry_dsn:
    import sentry_sdk
    from sentry_sdk.integrations.aiohttp import AioHttpIntegration
    from sentry_sdk.integrations.logging import LoggingIntegration

    sentry_sdk.init(
        dsn=_sentry_dsn,
        integrations=[
            AioHttpIntegration(),
            LoggingIntegration(
                level=logging.INFO,
                event_level=logging.ERROR,
            ),
        ],
        traces_sample_rate=float(os.environ.get('SENTRY_TRACES_SAMPLE_RATE', '0.1')),
        environment=os.environ.get('SENTRY_ENVIRONMENT', 'development'),
        send_default_pii=False,
    )
    logger.info("Sentry initialized for bot")
# ────────────────────────────────────────────────────────────────────────────

# Инициализация бота и диспетчера
bot_token = settings.TELEGRAM_BOT_TOKEN
if not bot_token:
    logger.warning("TELEGRAM_BOT_TOKEN не установлен в настройках!")
    bot = None
    dp = None
else:
    bot = Bot(token=bot_token)
    dp = Dispatcher(storage=MemoryStorage())


class BotFilterMiddleware(BaseMiddleware):
    """Middleware для фильтрации сообщений от ботов."""
    
    async def __call__(self, handler, event, data):
        # Когда middleware зарегистрирован через dp.message.middleware(),
        # event является Message объектом, а не Update
        # Когда зарегистрирован через dp.callback_query.middleware(),
        # event является CallbackQuery объектом
        if isinstance(event, Message):
            if event.from_user and event.from_user.is_bot:
                logger.info(f"[BotFilterMiddleware] Игнорируем сообщение от бота: {event.from_user.id}")
                return
        elif isinstance(event, CallbackQuery):
            if event.from_user and event.from_user.is_bot:
                logger.info(f"[BotFilterMiddleware] Игнорируем callback от бота: {event.from_user.id}")
                return
        elif isinstance(event, Update):
            # Если это Update объект (для совместимости)
            if event.message and event.message.from_user and event.message.from_user.is_bot:
                logger.info(f"[BotFilterMiddleware] Игнорируем сообщение от бота: {event.message.from_user.id}")
                return
            
            if event.callback_query and event.callback_query.from_user and event.callback_query.from_user.is_bot:
                logger.info(f"[BotFilterMiddleware] Игнорируем callback от бота: {event.callback_query.from_user.id}")
                return
        
        return await handler(event, data)


# Регистрируем middleware и обработчик блокировки бота
if dp:
    dp.message.middleware(BotFilterMiddleware())
    dp.callback_query.middleware(BotFilterMiddleware())

    @dp.error(ExceptionTypeFilter(TelegramForbiddenError))
    async def handle_user_blocked_bot(event: ErrorEvent):
        """Когда пользователь заблокировал бота — помечаем его неактивным в БД."""
        telegram_id = None
        update = event.update
        if update.message and update.message.from_user:
            telegram_id = update.message.from_user.id
        elif update.callback_query and update.callback_query.from_user:
            telegram_id = update.callback_query.from_user.id
        if telegram_id:
            try:
                def mark_user_blocked():
                    TelegramUser.objects.filter(telegram_id=telegram_id).update(
                        is_active=False, blocked_bot_at=timezone.now()
                    )
                await sync_to_async(mark_user_blocked)()
                logger.info("Пользователь %s заблокировал бота — помечен неактивным", telegram_id)
            except Exception as e:
                logger.warning("Не удалось обновить статус пользователя %s: %s", telegram_id, e)


class RegistrationStates(StatesGroup):
    """Состояния для регистрации пользователя."""
    waiting_for_language = State()
    waiting_for_name = State()
    waiting_for_user_type = State()
    waiting_for_privacy = State()
    waiting_for_phone = State()
    waiting_for_location = State()
    waiting_for_store_confirmation = State()  # JIP: sotuvchi uchun Store biriktirish
    waiting_for_promo_code = State()


class GiftRedemptionStates(StatesGroup):
    """Состояния для получения подарка."""
    selecting_gift = State()


def start_bot():
    """Запускает бота в отдельном потоке."""
    if not bot or not dp:
        logger.error("Бот не может быть запущен: TELEGRAM_BOT_TOKEN не установлен!")
        return
    
    async def run():
        try:
            logger.info("Запуск Telegram бота...")
            await dp.start_polling(bot)
        except Exception as e:
            logger.error(f"Error starting bot: {e}")
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(run())


def get_web_app_url():
    """Получает URL для Web App на основе настроек."""
    # Приоритет 1: Явно указанный WEB_APP_URL (для тестирования через ngrok)
    if settings.WEB_APP_URL and settings.WEB_APP_URL.startswith('https://'):
        return f"{settings.WEB_APP_URL.rstrip('/')}/api/webapp/"
    # Приоритет 2: WEBHOOK_URL (production)
    elif settings.WEBHOOK_URL and settings.WEBHOOK_URL.startswith('https://'):
        return f"{settings.WEBHOOK_URL.rstrip('/')}/api/webapp/"
    # Приоритет 3: ALLOWED_HOSTS в production
    elif not settings.DEBUG and settings.ALLOWED_HOSTS:
        domain = settings.ALLOWED_HOSTS[0]
        if domain and domain != 'localhost':
            return f"https://{domain}/api/webapp/"
    return None


def format_number(number):
    """
    Форматирует число с разделителями тысяч (пробелами).
    Пример: 1000000 -> "1 000 000"
    """
    try:
        num = int(float(number))
        return f"{num:,}".replace(",", " ")
    except (ValueError, TypeError):
        return str(number)


@sync_to_async
def get_or_create_user(telegram_id: int, username: str = None, first_name: str = None, last_name: str = None):
    """Получает или создает пользователя Telegram."""
    logger.info(f"[get_or_create_user] Получение/создание пользователя: telegram_id={telegram_id}, username={username}")
    
    # Не сохраняем имя автоматически - пользователь должен ввести его сам
    user, created = TelegramUser.objects.get_or_create(
        telegram_id=telegram_id,
        defaults={
            'username': username,
            # first_name и last_name не сохраняем автоматически
        }
    )
    
    logger.info(f"[get_or_create_user] Пользователь {'создан' if created else 'получен'}: id={user.id}, language={user.language}")
    
    # Обновляем username если он изменился
    if username and user.username != username:
        user.username = username
        user.save(update_fields=['username'])
        logger.info(f"[get_or_create_user] Username обновлен на: {username}")
    
    return user, created


@sync_to_async
def is_registration_complete(user):
    """Проверяет, завершена ли регистрация пользователя."""
    # Базовые проверки
    base_checks = (
        user.language and
        user.first_name and  # Добавляем проверку имени
        user.user_type and
        user.privacy_accepted and
        user.phone_number and
        user.latitude is not None and
        user.longitude is not None
    )
    
    # JIP: SmartUP ID o'rniga — sotuvchi uchun Store biriktirilganligini tekshiramiz
    if user.user_type == 'sotuvchi':
        # owned_stores reverse relation orqali tekshirish
        from asgiref.sync import sync_to_async
        has_store = await sync_to_async(
            lambda: user.owned_stores.filter(is_active=True).exists()
        )()
        result = base_checks and has_store
    else:
        result = base_checks

    logger.info(f"[is_registration_complete] Проверка регистрации для user_id={user.id}: "
                f"language={bool(user.language)}, first_name={bool(user.first_name)}, "
                f"user_type={bool(user.user_type)}, privacy_accepted={user.privacy_accepted}, "
                f"phone_number={bool(user.phone_number)}, location={user.latitude is not None and user.longitude is not None}, "
                f"result={result}")

    return result


@dp.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    """Обработчик команды /start."""
    # Игнорируем сообщения от ботов
    if message.from_user.is_bot:
        logger.info(f"[cmd_start] Игнорируем сообщение от бота: {message.from_user.id}")
        return
    
    logger.info(f"[cmd_start] Получена команда /start от пользователя {message.from_user.id}")

    # Парсим аргументы команды /start
    # Формат может быть: /start qr_ABC123 или /start EABC123
    args_text = message.text.split()[1:] if len(message.text.split()) > 1 else []
    qr_code_str = None
    
    # Проверяем формат ?start=qr_{qr_code} или ?start={qr_code}
    if args_text:
        arg = args_text[0]
        if arg.startswith('qr_') or arg.startswith('QR_'):
            # Нормализуем: убираем префикс 'qr_' или 'QR_' и приводим к верхнему регистру
            qr_code_str = arg[3:].upper().strip()  # Убираем префикс 'qr_' - это hash_code
        else:
            # Если формат без префикса, нормализуем регистр
            qr_code_str = arg.upper().strip()
        logger.info(f"[cmd_start] Обнаружен QR-код в аргументе: {qr_code_str}")
    
    user, is_new_user = await get_or_create_user(
        telegram_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name
    )
    
    logger.info(f"[cmd_start] Пользователь получен/создан: id={user.id}, telegram_id={user.telegram_id}, "
                f"is_new_user={is_new_user}, language={user.language}, first_name={user.first_name}, "
                f"user_type={user.user_type}, privacy_accepted={user.privacy_accepted}, "
                f"phone_number={user.phone_number}, latitude={user.latitude}, longitude={user.longitude}")
    
    # Проверяем, завершена ли регистрация
    registration_complete = await is_registration_complete(user)
    logger.info(f"[cmd_start] Регистрация завершена: {registration_complete}")
    
    # Если передан QR-код в аргументе
    if qr_code_str:
        if registration_complete:
            # Пользователь зарегистрирован - обрабатываем QR-код сразу
            logger.info(f"[cmd_start] Пользователь зарегистрирован, обрабатываем QR-код")
            await handle_qr_code_scan(message, user, qr_code_str, state)
            return
        else:
            # Пользователь не зарегистрирован - сохраняем QR-код в state для обработки после регистрации
            logger.info(f"[cmd_start] Пользователь не зарегистрирован, сохраняем QR-код в state")
            await state.update_data(pending_qr_code=qr_code_str)
    
    if registration_complete:
        # Пользователь уже зарегистрирован - показываем меню
        logger.info(f"[cmd_start] Пользователь уже зарегистрирован, показываем меню")
        await show_main_menu(message, user)
        await state.clear()
        return
    
    # Очищаем state для новой сессии регистрации
    await state.clear()
    logger.info(f"[cmd_start] Начинаем процесс регистрации")
    
    # Начинаем процесс регистрации с первого шага
    # Шаг 1: Выбор языка - всегда показываем приветствие если:
    # - это новый пользователь (только что создан) - даже если у него есть default язык
    # - или язык не выбран или пустой
    # ВАЖНО: Новые пользователи всегда должны выбрать язык, даже если в модели есть default
    if is_new_user or not user.language:
        logger.info(f"[cmd_start] Новый пользователь или язык не выбран (is_new_user={is_new_user}, user.language={user.language}), вызываем ask_language")
        await ask_language(message, user, state)
        return
    else:
        logger.info(f"[cmd_start] Язык уже выбран: {user.language}, пропускаем ask_language")
    
    # Шаг 2: Ввод имени - спрашиваем только после выбора языка
    if not user.first_name:
        logger.info(f"[cmd_start] Имя не указано, вызываем ask_name")
        await ask_name(message, user, state)
        return
    else:
        logger.info(f"[cmd_start] Имя указано: {user.first_name}, пропускаем ask_name")
    
    # Шаг 3: Выбор типа пользователя
    if not user.user_type:
        logger.info(f"[cmd_start] Тип пользователя не выбран, вызываем ask_user_type")
        await ask_user_type(message, user, state)
        return
    else:
        logger.info(f"[cmd_start] Тип пользователя выбран: {user.user_type}, пропускаем ask_user_type")
    
    # Шаг 3: Согласие на политику конфиденциальности
    if not user.privacy_accepted:
        logger.info(f"[cmd_start] Политика конфиденциальности не принята, вызываем ask_privacy_acceptance")
        await ask_privacy_acceptance(message, user, state)
        return
    else:
        logger.info(f"[cmd_start] Политика конфиденциальности принята, пропускаем ask_privacy_acceptance")
    
    # Шаг 4: Телефонный номер
    if not user.phone_number:
        logger.info(f"[cmd_start] Телефонный номер не указан, вызываем ask_phone")
        await ask_phone(message, user, state)
        return
    else:
        logger.info(f"[cmd_start] Телефонный номер указан, пропускаем ask_phone")
    
    # Шаг 5: Локация
    if user.latitude is None or user.longitude is None:
        logger.info(f"[cmd_start] Локация не указана, вызываем ask_location")
        await ask_location(message, user, state)
        return
    else:
        logger.info(f"[cmd_start] Локация указана, пропускаем ask_location")

    # JIP Шаг 6: Sotuvchi uchun Store biriktirilganligini tekshirish (SmartUP o'rniga)
    if user.user_type == 'sotuvchi':
        from asgiref.sync import sync_to_async
        has_store = await sync_to_async(
            lambda: user.owned_stores.filter(is_active=True).exists()
        )()
        if not has_store:
            await try_attach_seller_to_store(message, user, state)
            return

    # Шаг 7: Промокод (если еще не введен)
    # Промокод не обязателен, поэтому просто завершаем регистрацию
    logger.info(f"[cmd_start] Все шаги регистрации пройдены, показываем главное меню")
    await state.clear()
    await show_main_menu(message, user)


@dp.message(RegistrationStates.waiting_for_phone)
async def process_phone(message: Message, state: FSMContext):
    """Обработчик получения номера телефона."""
    # Игнорируем сообщения от ботов
    if message.from_user.is_bot:
        return
    
    if message.contact:
        phone_number = message.contact.phone_number
        
        @sync_to_async
        def update_phone():
            user = TelegramUser.objects.get(telegram_id=message.from_user.id)
            user.phone_number = phone_number
            user.save(update_fields=['phone_number'])
            return user
        
        user = await update_phone()
        await message.answer(get_text(user, 'PHONE_SAVED'))
        
        # Переходим к следующему шагу - локация
        await ask_location(message, user, state)
    else:
        @sync_to_async
        def get_user():
            return TelegramUser.objects.get(telegram_id=message.from_user.id)
        user = await get_user()
        await message.answer(get_text(user, 'USE_BUTTON_PHONE'))


@dp.message(RegistrationStates.waiting_for_location)
async def process_location(message: Message, state: FSMContext):
    """Обработчик получения локации."""
    # Игнорируем сообщения от ботов
    if message.from_user.is_bot:
        return
    
    if message.location:
        latitude = message.location.latitude
        longitude = message.location.longitude
        
        @sync_to_async
        def save_location_and_resolve_osm():
            user = TelegramUser.objects.get(telegram_id=message.from_user.id)
            user.latitude = latitude
            user.longitude = longitude
            user.save(update_fields=['latitude', 'longitude'])
            user.refresh_location_from_geocoder()
            user.save(update_fields=['region', 'district'])
            return user

        user = await save_location_and_resolve_osm()
        
        # Убираем клавиатуру с кнопкой геолокации
        remove_keyboard = types.ReplyKeyboardRemove()
        
        # JIP: Sotuvchi bo'lsa — Store'ga biriktirish (SmartUP o'rniga)
        if user.user_type == 'sotuvchi':
            await message.answer(get_text(user, 'LOCATION_SAVED'), reply_markup=remove_keyboard)
            await try_attach_seller_to_store(message, user, state)
        else:
            # Сообщение об успешной регистрации
            await message.answer(get_text(user, 'REGISTRATION_COMPLETE'), reply_markup=remove_keyboard)
            
            # Очищаем состояние и показываем главное меню
            await state.clear()
            await show_main_menu(message, user)
            # Затем обычным текстом просим ввести промокод (без установки состояния)
            await message.answer(get_text(user, 'SEND_PROMO_CODE'))
    else:
        @sync_to_async
        def get_user_for_location():
            return TelegramUser.objects.get(telegram_id=message.from_user.id)
        user = await get_user_for_location()
        await message.answer(get_text(user, 'USE_BUTTON_LOCATION'))


async def ask_language(message: Message, user, state: FSMContext):
    """Спрашивает у пользователя язык интерфейса."""
    logger.info(f"[ask_language] Вызывается для пользователя {user.telegram_id}, текущий язык: {user.language}")
    
    # Показываем приветствие на всех языках
    welcome_text = "Assalomu alaykum!\n«JIP» dasturiga xush kelibsiz.\nIltimos, qulay bo’lgan tilni tanlang:\n\nДобрый день!\nДобро пожаловать в программу «JIP».\nПожалуйста, выберите удобный для вас язык:"
    
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(
            text="🇺🇿 O‘zbekcha ",
            callback_data='lang_uz_latin'
        )],
        [types.InlineKeyboardButton(
            text="🇷🇺 Русский",
            callback_data='lang_ru'
        )],
    ])
    
    logger.info(f"[ask_language] Отправляем сообщение с выбором языка пользователю {user.telegram_id}")
    await message.answer(welcome_text, reply_markup=keyboard)
    await state.set_state(RegistrationStates.waiting_for_language)
    logger.info(f"[ask_language] Состояние установлено в waiting_for_language")


async def ask_name(message: Message, user, state: FSMContext):
    """Спрашивает у пользователя его имя."""
    await message.answer(get_text(user, 'ASK_NAME'))
    await state.set_state(RegistrationStates.waiting_for_name)


@dp.message(RegistrationStates.waiting_for_name)
async def process_name(message: Message, state: FSMContext):
    """Обработчик получения имени пользователя."""
    # Игнорируем сообщения от ботов
    if message.from_user.is_bot:
        return
    
    name = message.text.strip()
    
    # Проверяем, что имя не пустое и не слишком длинное
    if not name or len(name) < 2:
        @sync_to_async
        def get_user():
            return TelegramUser.objects.get(telegram_id=message.from_user.id)
        user = await get_user()
        await message.answer(get_text(user, 'NAME_TOO_SHORT'))
        return
    
    if len(name) > 255:
        name = name[:255]
    
    @sync_to_async
    def update_name():
        user = TelegramUser.objects.get(telegram_id=message.from_user.id)
        user.first_name = name
        user.save(update_fields=['first_name'])
        return user
    
    user = await update_name()
    await message.answer(get_text(user, 'NAME_SAVED'))
    
    # Переходим к следующему шагу - выбор типа пользователя
    await ask_user_type(message, user, state)


async def ask_user_type(message: Message, user, state: FSMContext):
    """Foydalanuvchi turini so'raydi (santenik yoki sotuvchi)."""
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(
            text=get_text(user, 'USER_TYPE_ELECTRICIAN'),
            callback_data='user_type_santenik'
        )],
        [types.InlineKeyboardButton(
            text=get_text(user, 'USER_TYPE_SELLER'),
            callback_data='user_type_sotuvchi'
        )],
    ])
    await message.answer(get_text(user, 'SELECT_USER_TYPE'), reply_markup=keyboard)
    await state.set_state(RegistrationStates.waiting_for_user_type)


async def send_video_instruction(chat_id: int, language: str, user_type: str):
    """Отправляет видео инструкцию пользователю (для electrician или seller, с учётом языка)."""
    logger.info(f"[send_video_instruction] chat_id={chat_id}, language={language}, user_type={user_type}")
    
    @sync_to_async
    def get_video_instruction():
        return VideoInstruction.objects.filter(is_active=True).first()
    
    instruction = await get_video_instruction()
    if not instruction:
        logger.warning("[send_video_instruction] Активная видео инструкция не найдена")
        return
    
    file_id = instruction.get_file_id(user_type, language)
    from .translations import TRANSLATIONS
    caption = TRANSLATIONS.get(language, TRANSLATIONS['uz_latin']).get('VIDEO_INSTRUCTION_CAPTION', '')
    
    def _get_thumb_input(thumb_file):
        """Возвращает FSInputFile для thumbnail или None."""
        if not thumb_file:
            return None
        try:
            path = thumb_file.path
            if path and os.path.exists(path):
                return types.FSInputFile(path)
        except (ValueError, OSError):
            pass
        alt = os.path.join(settings.MEDIA_ROOT, thumb_file.name) if thumb_file.name else None
        if alt and os.path.exists(alt):
            return types.FSInputFile(alt)
        return None
    
    if file_id:
        logger.info(f"[send_video_instruction] Используем file_id: {file_id}")
        try:
            await bot.send_video(chat_id=chat_id, video=file_id, caption=caption, request_timeout=300)
            logger.info("[send_video_instruction] Видео отправлено по file_id")
        except Exception as e:
            logger.error(f"[send_video_instruction] Ошибка по file_id: {e}")
            file_id = None
    
    if not file_id:
        video_file = instruction.get_video_file(user_type, language)
        if not video_file:
            logger.warning(f"[send_video_instruction] Видео не найдено для {user_type}/{language}")
            return
        
        thumb_file = instruction.get_thumb_file(user_type, language)
        thumb_input = await sync_to_async(_get_thumb_input)(thumb_file) if thumb_file else None
        
        try:
            video_path = video_file.path
            if os.path.exists(video_path):
                kwargs = dict(chat_id=chat_id, video=types.FSInputFile(video_path), caption=caption, request_timeout=300)
                if thumb_input:
                    kwargs['thumbnail'] = thumb_input
                sent_message = await bot.send_video(**kwargs)
            else:
                alt_path = os.path.join(settings.MEDIA_ROOT, video_file.name)
                if not os.path.exists(alt_path):
                    logger.error(f"[send_video_instruction] Файл не найден: {video_path}")
                    return
                kwargs = dict(chat_id=chat_id, video=types.FSInputFile(alt_path), caption=caption, request_timeout=300)
                if thumb_input:
                    kwargs['thumbnail'] = thumb_input
                sent_message = await bot.send_video(**kwargs)
            
            if sent_message.video and sent_message.video.file_id:
                new_file_id = sent_message.video.file_id
                def _save():
                    instruction.set_file_id(user_type, language, new_file_id)
                await sync_to_async(_save)()
                logger.info("[send_video_instruction] file_id сохранён")
        except asyncio.TimeoutError:
            logger.error("[send_video_instruction] Таймаут при отправке видео")
        except Exception as e:
            logger.error(f"[send_video_instruction] Ошибка: {e}", exc_info=True)


async def ask_privacy_acceptance(message: Message, user, state: FSMContext):
    """Спрашивает согласие на политику конфиденциальности."""
    from core.models import PrivacyPolicy
    from django.conf import settings
    import os
    
    logger.info(f"[ask_privacy_acceptance] Запрос политики для user_id={user.id}, language={user.language}")
    
    # Получаем активную политику конфиденциальности из базы данных
    @sync_to_async
    def get_privacy_policy():
        """Получает активную политику конфиденциальности."""
        return PrivacyPolicy.objects.filter(is_active=True).first()
    
    @sync_to_async
    def get_privacy_pdf():
        """Получает PDF файл политики конфиденциальности на языке пользователя."""
        policy = PrivacyPolicy.objects.filter(is_active=True).first()
        logger.info(f"[get_privacy_pdf] Политика найдена: {policy is not None}, user.language={user.language}")
        if policy:
            logger.info(f"[get_privacy_pdf] pdf_uz_latin: {bool(policy.pdf_uz_latin)}, pdf_ru: {bool(policy.pdf_ru)}")
            
            # Определяем язык пользователя (если не установлен, используем дефолтный)
            user_lang = user.language or 'uz_latin'
            logger.info(f"[get_privacy_pdf] Используемый язык: {user_lang}")
            
            # Узбекский язык может быть 'uz' или 'uz_latin'
            if user_lang in ['uz', 'uz_latin']:
                # Сначала пробуем узбекский
                if policy.pdf_uz_latin:
                    logger.info(f"[get_privacy_pdf] Возвращаем pdf_uz_latin: {policy.pdf_uz_latin.name}")
                    return policy.pdf_uz_latin
                # Если узбекского нет, пробуем русский
                elif policy.pdf_ru:
                    logger.info(f"[get_privacy_pdf] Нет uz_latin, возвращаем pdf_ru: {policy.pdf_ru.name}")
                    return policy.pdf_ru
            elif user_lang == 'ru':
                # Сначала пробуем русский
                if policy.pdf_ru:
                    logger.info(f"[get_privacy_pdf] Возвращаем pdf_ru: {policy.pdf_ru.name}")
                    return policy.pdf_ru
                # Если русского нет, пробуем узбекский
                elif policy.pdf_uz_latin:
                    logger.info(f"[get_privacy_pdf] Нет ru, возвращаем pdf_uz_latin: {policy.pdf_uz_latin.name}")
                    return policy.pdf_uz_latin
            
            # Если язык не определен, пробуем оба файла
            if policy.pdf_uz_latin:
                logger.info(f"[get_privacy_pdf] Язык не определен, возвращаем pdf_uz_latin: {policy.pdf_uz_latin.name}")
                return policy.pdf_uz_latin
            elif policy.pdf_ru:
                logger.info(f"[get_privacy_pdf] Язык не определен, возвращаем pdf_ru: {policy.pdf_ru.name}")
                return policy.pdf_ru
                
        logger.info(f"[get_privacy_pdf] PDF не найден")
        return None
    
    # Получаем PDF файл политики конфиденциальности
    pdf_file = await get_privacy_pdf()
    logger.info(f"[ask_privacy_acceptance] PDF файл получен: {pdf_file is not None}")
    
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(
            text=get_text(user, 'ACCEPT_PRIVACY'),
            callback_data='accept_privacy'
        )],
        [types.InlineKeyboardButton(
            text=get_text(user, 'DECLINE_PRIVACY'),
            callback_data='decline_privacy'
        )],
    ])
    
    # Отправляем PDF файл политики конфиденциальности
    if pdf_file:
        try:
            # Получаем полный путь к файлу через свойство .path Django FileField
            pdf_path = pdf_file.path
            logger.info(f"[ask_privacy_acceptance] Путь к PDF: {pdf_path}")
            
            # Проверяем существование файла
            if os.path.exists(pdf_path):
                logger.info(f"[ask_privacy_acceptance] Файл существует, отправляем PDF")
                # Отправляем PDF как документ
                await message.answer_document(
                    types.FSInputFile(pdf_path),
                    caption=get_text(user, 'PRIVACY_POLICY_TEXT'),
                    reply_markup=keyboard
                )
            else:
                # Если файл не найден, пробуем альтернативный путь
                alt_path = os.path.join(settings.MEDIA_ROOT, pdf_file.name)
                logger.info(f"[ask_privacy_acceptance] Пробуем альтернативный путь: {alt_path}")
                if os.path.exists(alt_path):
                    logger.info(f"[ask_privacy_acceptance] Файл найден по альтернативному пути, отправляем PDF")
                    await message.answer_document(
                        types.FSInputFile(alt_path),
                        caption=get_text(user, 'PRIVACY_POLICY_TEXT'),
                        reply_markup=keyboard
                    )
                else:
                    # Если файл не найден, отправляем сообщение об ошибке
                    logger.warning(f"[ask_privacy_acceptance] PDF файл не найден на диске. Путь: {pdf_path}, Альтернативный: {alt_path}")
                    await message.answer(get_text(user, 'PRIVACY_POLICY_TEXT'), reply_markup=keyboard)
        except Exception as e:
            logger.error(f"[ask_privacy_acceptance] Ошибка при отправке PDF: {e}")
            # В случае ошибки отправляем текстовое сообщение
            await message.answer(get_text(user, 'PRIVACY_POLICY_TEXT'), reply_markup=keyboard)
    else:
        # Если PDF файл не загружен, отправляем текстовое сообщение (fallback)
        logger.warning(f"[ask_privacy_acceptance] PDF файл не загружен в базу данных для языка {user.language}")
        await message.answer(get_text(user, 'PRIVACY_POLICY_TEXT'), reply_markup=keyboard)
    
    await state.set_state(RegistrationStates.waiting_for_privacy)


async def ask_phone(message: Message, user, state: FSMContext):
    """Спрашивает номер телефона."""
    # ReplyKeyboard с кнопкой запроса контакта
    reply_keyboard = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text=get_text(user, 'SEND_PHONE_BUTTON'), request_contact=True)]
        ],
        resize_keyboard=True
    )
    
    # InlineKeyboard с подсказкой для пользователей TelegramPlus
    inline_text = "👇 " + (get_text(user, 'HINT_USE_BUTTON_BELOW') if user.language == 'ru' 
                          else "Quyidagi tugmani bosing")
    inline_keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text=inline_text, callback_data='hint_phone')]
    ])
    
    await message.answer(
        get_text(user, 'SEND_PHONE'), 
        reply_markup=reply_keyboard
    )
    # Отправляем дополнительное сообщение с InlineKeyboard-подсказкой
    await message.answer(
        "⬇️ " + (get_text(user, 'USE_BUTTON_PHONE') if hasattr(user, 'language') else "Используйте кнопку внизу"),
        reply_markup=inline_keyboard
    )
    await state.set_state(RegistrationStates.waiting_for_phone)


async def ask_location(message: Message, user, state: FSMContext):
    """Спрашивает локацию."""
    # ReplyKeyboard с кнопкой запроса локации
    reply_keyboard = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="📍 " + get_text(user, 'SEND_LOCATION').replace('📍 ', ''), request_location=True)]
        ],
        resize_keyboard=True
    )
    
    # InlineKeyboard с подсказкой для пользователей TelegramPlus
    inline_text = "👇 " + (get_text(user, 'HINT_USE_BUTTON_BELOW') if user.language == 'ru' 
                          else "Quyidagi tugmani bosing")
    inline_keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text=inline_text, callback_data='hint_location')]
    ])
    
    await message.answer(
        get_text(user, 'SEND_LOCATION'), 
        reply_markup=reply_keyboard
    )
    # Отправляем дополнительное сообщение с InlineKeyboard-подсказкой
    await message.answer(
        "⬇️ " + (get_text(user, 'USE_BUTTON_LOCATION') if hasattr(user, 'language') else "Используйте кнопку внизу"),
        reply_markup=inline_keyboard
    )
    await state.set_state(RegistrationStates.waiting_for_location)


async def try_attach_seller_to_store(message: Message, user, state: FSMContext):
    """JIP: Sotuvchi telefon raqami orqali Store'ga biriktirilishini tekshiradi.

    - Telefon raqami `Store.owner.phone_number` orqali topiladi
    - Topilsa: tasdiqlash so'raydi
    - Topilmasa: admin kontakti yuboriladi
    """
    from core.models import Store, AdminContactSettings

    @sync_to_async
    def find_store_for_seller():
        return Store.objects.filter(
            owner=user, is_active=True,
        ).first()

    @sync_to_async
    def get_admin_contact():
        s = AdminContactSettings.objects.first()
        return (s.telegram_username if s and s.telegram_username else '@admin')

    store = await find_store_for_seller()
    admin_contact = await get_admin_contact()

    if store is None:
        # Owner ulanmagan — telefon orqali qidirib ko'ramiz
        @sync_to_async
        def find_store_by_phone():
            return Store.objects.filter(
                phone=user.phone_number, is_active=True, owner__isnull=True,
            ).first()
        store = await find_store_by_phone()

        if store is None:
            await message.answer(
                get_text(user, 'SELLER_STORE_NOT_FOUND').format(admin_contact=admin_contact)
            )
            await state.clear()
            return

        # Auto-attach
        @sync_to_async
        def attach_owner():
            store.owner = user
            store.save(update_fields=['owner'])
        await attach_owner()

    await message.answer(
        get_text(user, 'SELLER_STORE_CONFIRM').format(
            store_name=store.name, address=store.address,
        ),
        parse_mode='HTML',
    )
    await message.answer(
        get_text(user, 'SELLER_STORE_CONFIRMED').format(store_name=store.name),
        parse_mode='HTML',
    )
    await state.clear()
    await show_main_menu(message, user)


async def ask_promo_code(message: Message, user, state: FSMContext):
    """Спрашивает промокод."""
    await message.answer(get_text(user, 'SEND_PROMO_CODE'))
    await state.set_state(RegistrationStates.waiting_for_promo_code)


@dp.message(RegistrationStates.waiting_for_promo_code)
async def process_promo_code(message: Message, state: FSMContext):
    """Обработчик получения промокода."""
    # Игнорируем сообщения от ботов
    if message.from_user.is_bot:
        return
    
    promo_code = message.text.strip() if message.text else ""
    
    @sync_to_async
    def get_user():
        return TelegramUser.objects.get(telegram_id=message.from_user.id)
    
    user = await get_user()
    
    # Проверяем, не является ли это командой меню
    all_menu_commands = [
        TRANSLATIONS['uz_latin']['MY_BALANCE'],
        TRANSLATIONS['ru']['MY_BALANCE'],
        TRANSLATIONS['uz_latin']['GIFTS'],
        TRANSLATIONS['ru']['GIFTS'],
        TRANSLATIONS['uz_latin']['TOP_LEADERS'],
        TRANSLATIONS['ru']['TOP_LEADERS'],
        TRANSLATIONS['uz_latin']['TOP_LEADERS_MONTH'],
        TRANSLATIONS['ru']['TOP_LEADERS_MONTH'],
        TRANSLATIONS['uz_latin']['LANGUAGE'],
        TRANSLATIONS['ru']['LANGUAGE'],
        TRANSLATIONS['uz_latin']['ENTER_PROMO_CODE'],
        TRANSLATIONS['ru']['ENTER_PROMO_CODE'],
    ]
    
    # Если это команда меню, выходим из состояния и обрабатываем как обычное сообщение
    if message.text in all_menu_commands:
        await state.clear()
        await handle_message(message, state)
        return
    
    # Проверяем, есть ли ожидающий QR-код из state (передан при /start)
    state_data = await state.get_data()
    pending_qr_code = state_data.get('pending_qr_code')
    
    # Если промокод введен, проверяем его как QR-код
    # Нормализуем регистр для поиска (case-insensitive)
    qr_code_to_check = (promo_code.upper().strip() if promo_code else None) or (pending_qr_code.upper().strip() if pending_qr_code else None)
    
    if qr_code_to_check:
        # Перед любыми проверками смотрим, не заблокирован ли пользователь по промокодам
        blocked, block_type, blocked_until = await sync_to_async(user.is_promo_code_blocked)()
        if blocked:
            if block_type == 'permanent':
                msg = get_text(user, 'PROMO_BLOCKED_PERMANENT')
            else:
                msg = get_text(user, 'PROMO_BLOCKED_1_DAY')
            await message.answer(msg)
            await state.clear()
            return

        # Проверяем QR-код напрямую, чтобы определить результат до завершения регистрации
        @sync_to_async
        def check_qr_code():
            """Проверяет существование QR-кода в базе."""
            # Нормализуем ввод: приводим к верхнему регистру для поиска
            qr_code_normalized = qr_code_to_check.upper().strip()
            
            try:
                # Сначала ищем по полному коду (E-ABC123 или D-ABC123) - нечувствительно к регистру
                qr_code = QRCode.objects.get(code__iexact=qr_code_normalized, is_deleted=False)
                return {'found': True, 'qr_code': qr_code}
            except QRCode.DoesNotExist:
                # Если не нашли, пробуем найти по hash_code (без префикса) - нечувствительно к регистру
                try:
                    qr_code = QRCode.objects.get(hash_code__iexact=qr_code_normalized, is_deleted=False)
                    return {'found': True, 'qr_code': qr_code}
                except QRCode.DoesNotExist:
                    return {'found': False}
        
        qr_check_result = await check_qr_code()
        
        if not qr_check_result.get('found'):
            # QR-код не найден — регистрируем неверную попытку
            await sync_to_async(user.register_invalid_promo_attempt)(source='bot', raw_code=promo_code or pending_qr_code or '')
            await message.answer(get_text(user, 'QR_NOT_FOUND'))
            await ask_promo_code(message, user, state)
            return
        
        # QR-код найден - обрабатываем его через handle_qr_code_scan
        # Временно сохраняем состояние
        await state.update_data(pending_qr_code=qr_code_to_check)
        
        # Обрабатываем QR-код
        await handle_qr_code_scan(message, user, qr_code_to_check, state)
        
        # Проверяем, завершена ли регистрация после обработки QR-кода
        @sync_to_async
        def get_user_for_check():
            return TelegramUser.objects.get(telegram_id=message.from_user.id)
        
        user_for_check = await get_user_for_check()
        registration_complete = await is_registration_complete(user_for_check)
        
        if registration_complete:
            # Регистрация завершена, handle_qr_code_scan уже обработал QR-код и показал меню
            await state.clear()
            return
        else:
            # QR-код был обработан, но регистрация еще не завершена
            await state.clear()
            return
    
    # Если промокод не введен и нет ожидающего QR-кода, завершаем регистрацию
    await state.clear()
    
    # Убираем клавиатуру
    remove_keyboard = types.ReplyKeyboardRemove()
    await message.answer(get_text(user, 'REGISTRATION_COMPLETE_MESSAGE'), reply_markup=remove_keyboard)
    
    # Показываем главное меню
    await show_main_menu(message, user)


@dp.callback_query(lambda c: c.data.startswith('lang_'))
async def process_language_selection(callback: CallbackQuery, state: FSMContext):
    """Обрабатывает выбор языка."""
    # Игнорируем callback от ботов
    if callback.from_user.is_bot:
        return
    
    logger.info(f"[process_language_selection] Получен callback: {callback.data} от пользователя {callback.from_user.id}")
    
    try:
        language = callback.data.split('_', 1)[1]  # uz_latin или ru (берем всё после 'lang_')
        logger.info(f"[process_language_selection] Выбранный язык: {language}")
        
        @sync_to_async
        def update_language_and_check_registration():
            # get_or_create: пользователь может прийти из Web App (resend_registration_step)
            # без предварительной отправки /start — в таком случае создаём запись
            user, created = TelegramUser.objects.get_or_create(
                telegram_id=callback.from_user.id,
                defaults={
                    'username': callback.from_user.username,
                }
            )
            if created:
                logger.info(f"[process_language_selection] Создан новый пользователь: telegram_id={callback.from_user.id}")
            logger.info(f"[process_language_selection] Текущий язык пользователя до обновления: {user.language}")
            user.language = language
            user.save(update_fields=['language'])
            logger.info(f"[process_language_selection] Язык пользователя обновлен на: {user.language}")
            # JIP: sotuvchi uchun Store biriktirilganligini tekshiramiz
            base_checks = (
                user.language and
                user.first_name and
                user.user_type and
                user.privacy_accepted and
                user.phone_number and
                user.latitude is not None and
                user.longitude is not None
            )
            if user.user_type == 'sotuvchi':
                is_registered = base_checks and user.owned_stores.filter(is_active=True).exists()
            else:
                is_registered = base_checks
            return user, is_registered
        
        user, is_registered = await update_language_and_check_registration()
        logger.info(f"[process_language_selection] Регистрация завершена: {is_registered}")
        
        await callback.answer(get_text(user, 'LANGUAGE_CHANGED'))
        await _safe_delete_message(callback.message)
        
        # Видео инструкция отправляется после выбора типа пользователя (electrician/seller)
        if is_registered:
            # Пользователь уже зарегистрирован - показываем обновленное меню
            logger.info(f"[process_language_selection] Пользователь зарегистрирован, показываем меню")
            await state.clear()
            
            # Получаем баллы пользователя
            @sync_to_async
            def get_user_points():
                user_obj = TelegramUser.objects.get(telegram_id=callback.from_user.id)
                return user_obj.points
            
            points = await get_user_points()
            
            # Создаем reply keyboard кнопки
            keyboard_buttons = []
            
            # Определяем URL для Web App
            web_app_url = get_web_app_url()
            
            # Добавляем кнопки меню
            keyboard_buttons.extend([
                [types.KeyboardButton(text=get_text(user, 'GIFTS'))],
                [
                    types.KeyboardButton(text=get_text(user, 'MY_BALANCE')),
                    types.KeyboardButton(text=get_text(user, 'TOP_LEADERS')),
                    types.KeyboardButton(text=get_text(user, 'TOP_LEADERS_MONTH')),
                ],
                [types.KeyboardButton(text=get_text(user, 'ENTER_PROMO_CODE'))],
                [types.KeyboardButton(text=get_text(user, 'LANGUAGE'))],
            ])
            
            keyboard = types.ReplyKeyboardMarkup(
                keyboard=keyboard_buttons,
                resize_keyboard=True
            )
            
            # Создаем inline кнопку для Web App
            inline_keyboard = None
            if web_app_url:
                try:
                    web_app_button = types.InlineKeyboardButton(
                        text=get_text(user, 'MY_GIFTS'),
                        web_app=types.WebAppInfo(url=web_app_url)
                    )
                    inline_keyboard = types.InlineKeyboardMarkup(
                        inline_keyboard=[[web_app_button]]
                    )
                except Exception as e:
                    logger.warning(f"Не удалось создать Web App inline кнопку: {e}")
            
            # Отправляем сообщение с обновленной клавиатурой
            await bot.send_message(
                chat_id=callback.from_user.id,
                text=get_text(user, 'MAIN_MENU', points=format_number(points)),
                reply_markup=keyboard
            )
            
            # Отправляем отдельное сообщение с inline кнопкой для Web App
            if inline_keyboard:
                await bot.send_message(
                    chat_id=callback.from_user.id,
                    text=get_text(user, 'OPEN_WEB_APP'),
                    reply_markup=inline_keyboard
                )
        else:
            # Регистрация не завершена - продолжаем регистрацию
            logger.info(f"[process_language_selection] Регистрация не завершена, продолжаем процесс регистрации")
            # Используем callback.message для отправки следующего вопроса
            # message.answer() создает новое сообщение, даже если исходное было удалено
            # Шаг 2: Ввод имени - спрашиваем только после выбора языка
            if not user.first_name:
                logger.info(f"[process_language_selection] Имя не указано, вызываем ask_name")
                await ask_name(callback.message, user, state)
            # Шаг 3: Выбор типа пользователя
            elif not user.user_type:
                logger.info(f"[process_language_selection] Тип пользователя не выбран, вызываем ask_user_type")
                await ask_user_type(callback.message, user, state)
            # Шаг 4: Согласие на политику конфиденциальности
            elif not user.privacy_accepted:
                logger.info(f"[process_language_selection] Политика конфиденциальности не принята, вызываем ask_privacy_acceptance")
                await ask_privacy_acceptance(callback.message, user, state)
            # Шаг 5: Телефонный номер
            elif not user.phone_number:
                logger.info(f"[process_language_selection] Телефонный номер не указан, вызываем ask_phone")
                await ask_phone(callback.message, user, state)
            # Шаг 6: Локация
            elif user.latitude is None or user.longitude is None:
                logger.info(f"[process_language_selection] Локация не указана, вызываем ask_location")
                await ask_location(callback.message, user, state)
            # JIP: Sotuvchi uchun Store biriktirish
            elif user.user_type == 'sotuvchi' and not user.owned_stores.filter(is_active=True).exists():
                logger.info(f"[process_language_selection] Sotuvchi uchun Store biriktirilmagan, try_attach_seller_to_store")
                await try_attach_seller_to_store(callback.message, user, state)
            # Шаг 8: Промокод (не обязателен)
            else:
                logger.info(f"[process_language_selection] Все шаги регистрации пройдены, показываем главное меню")
                await state.clear()
                await show_main_menu(callback.message, user)
    except TelegramBadRequest as e:
        msg = str(e).lower()
        if "can't be deleted for everyone" in msg or "message to delete not found" in msg:
            logger.debug("[process_language_selection] Удаление сообщения недоступно (игнор): %s", e)
        else:
            logger.error(f"[process_language_selection] Ошибка при обработке выбора языка: {e}", exc_info=True)
            await callback.answer("Произошла ошибка. Попробуйте еще раз.")
    except Exception as e:
        logger.error(f"[process_language_selection] Ошибка при обработке выбора языка: {e}", exc_info=True)
        await callback.answer("Произошла ошибка. Попробуйте еще раз.")


@dp.callback_query(lambda c: c.data.startswith('user_type_'))
async def process_user_type_selection(callback: CallbackQuery, state: FSMContext):
    """Обрабатывает выбор типа пользователя."""
    # Игнорируем callback от ботов
    if callback.from_user.is_bot:
        return
    
    user_type = callback.data.split('_')[2]  # santenik yoki sotuvchi
    
    @sync_to_async
    def update_user_type():
        user = TelegramUser.objects.get(telegram_id=callback.from_user.id)
        user.user_type = user_type
        user.save(update_fields=['user_type'])
        return user
    
    user = await update_user_type()
    
    await callback.answer(get_text(user, 'USER_TYPE_SAVED'))
    await _safe_delete_message(callback.message)
    
    # Отправляем видео инструкцию для выбранного типа (electrician/seller) и языка
    try:
        await send_video_instruction(callback.from_user.id, user.language or 'uz_latin', user_type)
    except Exception as e:
        logger.error(f"[process_user_type_selection] Ошибка при отправке видео: {e}", exc_info=True)
    
    # Переходим к следующему шагу - согласие на политику конфиденциальности
    await ask_privacy_acceptance(callback.message, user, state)


@dp.callback_query(lambda c: c.data in ['hint_phone', 'hint_location'])
async def process_hint_callback(callback: CallbackQuery):
    """Обрабатывает нажатия на подсказки для телефона и локации."""
    if callback.from_user.is_bot:
        return
    
    @sync_to_async
    def get_user():
        return TelegramUser.objects.get(telegram_id=callback.from_user.id)
    
    user = await get_user()
    
    if callback.data == 'hint_phone':
        hint_text = get_text(user, 'USE_BUTTON_PHONE')
    else:  # hint_location
        hint_text = get_text(user, 'USE_BUTTON_LOCATION')
    
    await callback.answer(hint_text, show_alert=True)


@dp.callback_query(lambda c: c.data in ['accept_privacy', 'decline_privacy'])
async def process_privacy_acceptance(callback: CallbackQuery, state: FSMContext):
    """Обрабатывает согласие на политику конфиденциальности."""
    # Игнорируем callback от ботов
    if callback.from_user.is_bot:
        return
    
    if callback.data == 'decline_privacy':
        @sync_to_async
        def get_user():
            return TelegramUser.objects.get(telegram_id=callback.from_user.id)
        user = await get_user()
        await callback.answer(get_text(user, 'PRIVACY_DECLINED'))
        await callback.message.answer(get_text(user, 'PRIVACY_REQUIRED'))
        return
    
    @sync_to_async
    def update_privacy():
        user = TelegramUser.objects.get(telegram_id=callback.from_user.id)
        user.privacy_accepted = True
        user.save(update_fields=['privacy_accepted'])
        return user
    
    user = await update_privacy()
    
    await callback.answer(get_text(user, 'PRIVACY_ACCEPTED'))
    await _safe_delete_message(callback.message)
    
    # Переходим к следующему шагу - телефонный номер
    await ask_phone(callback.message, user, state)


async def handle_qr_code_scan(message: Message, user, qr_code_str: str, state: FSMContext):
    """Обрабатывает сканирование QR-кода."""
    try:
        @sync_to_async
        def process_qr_scan():
            from django.utils import timezone
            from django.db import transaction
            from datetime import datetime, time as dt_time
            
            # Используем транзакцию для атомарности операций
            with transaction.atomic():
                # Нормализуем ввод: приводим к верхнему регистру для поиска
                qr_code_str_normalized = qr_code_str.upper().strip()
                
                # Ищем QR-код по коду или hash_code (case-insensitive)
                qr_code = None
                try:
                    # Сначала ищем по полному коду (E-ABC123 или D-ABC123) - нечувствительно к регистру
                    qr_code = QRCode.objects.get(code__iexact=qr_code_str_normalized, is_deleted=False)
                except QRCode.DoesNotExist:
                    # Если не нашли, пробуем найти по hash_code (без префикса) - нечувствительно к регистру
                    try:
                        qr_code = QRCode.objects.get(hash_code__iexact=qr_code_str_normalized, is_deleted=False)
                    except QRCode.DoesNotExist:
                        # QR-код не найден, возвращаем ошибку без создания попытки
                        user.register_invalid_promo_attempt(source='bot', raw_code=qr_code_str)
                        return {'error': 'not_found'}
                
                # Проверяем, не был ли уже отсканирован
                if qr_code.is_scanned:
                    # Создаем запись о неудачной попытке
                    QRCodeScanAttempt.objects.create(
                        user=user,
                        qr_code=qr_code,
                        is_successful=False
                    )
                    user.register_invalid_promo_attempt(source='bot', raw_code=qr_code_str)
                    return {'error': 'already_scanned'}
                
                # JIP: Faqat santenik QR kodni skanlashi mumkin
                if user.user_type != 'santenik':
                    QRCodeScanAttempt.objects.create(user=user, qr_code=qr_code, is_successful=False)
                    user.register_invalid_promo_attempt(source='bot', raw_code=qr_code_str)
                    return {'error': 'wrong_type'}

                # Отмечаем QR-код как отсканированный
                qr_code.is_scanned = True
                qr_code.scanned_at = timezone.now()
                qr_code.scanned_by = user
                qr_code.save(update_fields=['is_scanned', 'scanned_at', 'scanned_by'])

                # Выдаём билет месячного розыгрыша (по одному на каждый QR)
                from core.monthly_promo import assign_monthly_ticket, count_user_chances
                assign_monthly_ticket(qr_code=qr_code, user=user)
                monthly_chances = count_user_chances(user=user)
                
                # Создаем запись об успешной попытке
                QRCodeScanAttempt.objects.create(
                    user=user,
                    qr_code=qr_code,
                    is_successful=True
                )
                # Фиксируем успешный промокод
                user.register_successful_promo(raw_code=qr_code_str, source='bot')
                
                # Инвалидируем кеш и пересчитываем баллы из БД (как в webapp)
                user.invalidate_points_cache()
                total_points = user.calculate_points(force=True)
                
                return {
                    'success': True,
                    'points': qr_code.points,
                    'total_points': total_points,
                    'monthly_chances': monthly_chances,
                }
        
        # Перед обработкой проверяем блокировку по промокодам
        blocked, block_type, blocked_until = await sync_to_async(user.is_promo_code_blocked)()
        if blocked:
            if block_type == 'permanent':
                await message.answer(get_text(user, 'PROMO_BLOCKED_PERMANENT'))
            else:
                await message.answer(get_text(user, 'PROMO_BLOCKED_1_DAY'))
            return

        result = await process_qr_scan()
        
        # Проверяем, завершена ли регистрация (для определения, нужно ли показывать меню или продолжать регистрацию)
        @sync_to_async
        def get_user_for_reg_check():
            return TelegramUser.objects.get(telegram_id=message.from_user.id)
        
        user_for_reg_check = await get_user_for_reg_check()
        registration_complete = await is_registration_complete(user_for_reg_check)
        
        if result.get('error') == 'not_found':
            await message.answer(get_text(user, 'QR_NOT_FOUND'))
            if registration_complete:
                await show_main_menu(message, user)
            else:
                # Если регистрация не завершена, продолжаем ожидать промокод
                await ask_promo_code(message, user, state)
        elif result.get('error') == 'already_scanned':
            await message.answer(get_text(user, 'QR_ALREADY_SCANNED'))
            if registration_complete:
                await show_main_menu(message, user)
            else:
                # Если регистрация не завершена, продолжаем ожидать промокод
                await ask_promo_code(message, user, state)
        elif result.get('error') == 'wrong_type':
            await message.answer(get_text(user, 'QR_WRONG_TYPE'))
            if registration_complete:
                await show_main_menu(message, user)
            else:
                # Если регистрация не завершена, продолжаем ожидать промокод
                await ask_promo_code(message, user, state)
        elif result.get('success'):
            chances_line = ''
            if result.get('monthly_chances') is not None:
                chances_line = '\n\n' + get_text(user, 'MONTHLY_CHANCES_LINE', count=result['monthly_chances'])
            await message.answer(get_text(user, 'QR_ACTIVATED',
                points=format_number(result['points']),
                total_points=format_number(result['total_points'])
            ) + chances_line)
            # Если пользователь еще не зарегистрирован, продолжаем регистрацию
            if not user.phone_number or not user.latitude:
                keyboard = types.ReplyKeyboardMarkup(
                    keyboard=[
                        [types.KeyboardButton(text=get_text(user, 'SEND_PHONE').split(':')[0] + "...", request_contact=True)]
                    ],
                    resize_keyboard=True
                )
                await message.answer(get_text(user, 'SEND_PHONE'), reply_markup=keyboard)
                await state.set_state(RegistrationStates.waiting_for_phone)
            else:
                await show_main_menu(message, user)
        
    except Exception as e:
        logger.error(f"Error processing QR code scan: {e}")
        await message.answer(get_text(user, 'QR_ERROR'))


async def show_main_menu(message: Message, user: TelegramUser):
    """Показывает главное меню — разное для santenik и sotuvchi."""
    if user.user_type == 'sotuvchi':
        await show_seller_menu(message, user)
    else:
        await show_santenik_menu(message, user)


async def show_santenik_menu(message: Message, user: TelegramUser):
    """Santenik asosiy menyusi."""
    @sync_to_async
    def get_points():
        return TelegramUser.objects.get(telegram_id=message.from_user.id).points

    points = await get_points()
    web_app_url = get_web_app_url()

    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text=get_text(user, 'GIFTS'))],
            [
                types.KeyboardButton(text=get_text(user, 'MY_BALANCE')),
                types.KeyboardButton(text=get_text(user, 'TOP_LEADERS')),
                types.KeyboardButton(text=get_text(user, 'TOP_LEADERS_MONTH')),
            ],
            [types.KeyboardButton(text=get_text(user, 'ENTER_PROMO_CODE'))],
            [types.KeyboardButton(text=get_text(user, 'LANGUAGE'))],
        ],
        resize_keyboard=True,
    )

    await message.answer(
        get_text(user, 'MAIN_MENU', points=format_number(points)),
        reply_markup=keyboard,
    )

    if web_app_url:
        try:
            inline_kb = types.InlineKeyboardMarkup(inline_keyboard=[[
                types.InlineKeyboardButton(
                    text=get_text(user, 'MY_GIFTS'),
                    web_app=types.WebAppInfo(url=web_app_url),
                )
            ]])
            await message.answer(get_text(user, 'OPEN_WEB_APP'), reply_markup=inline_kb)
        except Exception as e:
            logger.warning(f"Web App inline button error: {e}")


async def show_seller_menu(message: Message, user: TelegramUser):
    """Sotuvchi asosiy menyusi."""
    @sync_to_async
    def get_seller_data():
        u = TelegramUser.objects.select_related('owned_stores__region').get(
            telegram_id=message.from_user.id
        )
        store = u.owned_stores.filter(is_active=True).select_related('region').first()
        return u.points, store

    points, store = await get_seller_data()
    web_app_url = get_web_app_url()

    store_name = store.name if store else '—'
    menu_text = get_text(
        user, 'SELLER_MAIN_MENU',
        name=user.first_name or '',
        store=store_name,
        points=format_number(points),
    )

    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text=get_text(user, 'SELLER_MY_BALANCE'))],
            [types.KeyboardButton(text=get_text(user, 'SELLER_MY_STORE'))],
            [types.KeyboardButton(text=get_text(user, 'SELLER_CONTACT_ADMIN'))],
            [types.KeyboardButton(text=get_text(user, 'LANGUAGE'))],
        ],
        resize_keyboard=True,
    )

    await message.answer(menu_text, reply_markup=keyboard, parse_mode='HTML')

    if web_app_url:
        try:
            seller_url = f"{web_app_url.rstrip('/')}/seller/"
            inline_kb = types.InlineKeyboardMarkup(inline_keyboard=[[
                types.InlineKeyboardButton(
                    text=get_text(user, 'SELLER_WEBAPP_BUTTON'),
                    web_app=types.WebAppInfo(url=seller_url),
                )
            ]])
            await message.answer(get_text(user, 'SELLER_OPEN_WEBAPP'), reply_markup=inline_kb)
        except Exception as e:
            logger.warning(f"Seller Web App inline button error: {e}")


@dp.message()
async def handle_message(message: Message, state: FSMContext = None):
    """Универсальный обработчик сообщений."""
    # Игнорируем сообщения от ботов
    if message.from_user.is_bot:
        return
    
    @sync_to_async
    def get_user():
        return TelegramUser.objects.get(telegram_id=message.from_user.id)
    
    try:
        user = await get_user()
    except TelegramUser.DoesNotExist:
        # Пользователь ещё не зарегистрирован — просим отправить /start
        no_user = SimpleNamespace(language='uz_latin')
        await message.answer(get_text(no_user, 'PLEASE_START'))
        return
    
    # Если пользователь в состоянии регистрации, не обрабатываем как QR-код
    if state:
        current_state = await state.get_state()
        if current_state in [
            RegistrationStates.waiting_for_phone,
            RegistrationStates.waiting_for_location,
            RegistrationStates.waiting_for_user_type,
            RegistrationStates.waiting_for_store_confirmation,
        ]:
            # Пропускаем обработку, пусть обрабатывают соответствующие handlers
            return

    # JIP: Sotuvchi uchun Store biriktirilmagan bo'lsa — qaytaramiz
    if user.user_type == 'sotuvchi':
        has_store = await sync_to_async(
            lambda: user.owned_stores.filter(is_active=True).exists()
        )()
        if not has_store:
            logger.info(
                f"[handle_message] Sotuvchi {user.telegram_id} Store'siz — "
                "try_attach_seller_to_store"
            )
            await try_attach_seller_to_store(message, user, state)
            return

    # Пользователь не завершил регистрацию, но FSM-состояние могло сброситься (бот перезапуск и т.д.).
    # Принимаем контакт и локацию независимо от состояния.
    registration_incomplete = not await is_registration_complete(user)
    if registration_incomplete:
        if message.contact and not user.phone_number:
            # Пользователь отправил контакт (кнопка или из списка контактов) — сохраняем
            phone_number = message.contact.phone_number
            @sync_to_async
            def update_phone():
                u = TelegramUser.objects.get(telegram_id=message.from_user.id)
                u.phone_number = phone_number
                u.save(update_fields=['phone_number'])
                return u
            user = await update_phone()
            await message.answer(get_text(user, 'PHONE_SAVED'))
            await ask_location(message, user, state)
            return
        if message.location and user.phone_number and (user.latitude is None or user.longitude is None):
            # Пользователь отправил геолокацию
            lat, lon = message.location.latitude, message.location.longitude
            @sync_to_async
            def update_loc():
                u = TelegramUser.objects.get(telegram_id=message.from_user.id)
                u.latitude, u.longitude = lat, lon
                u.save(update_fields=['latitude', 'longitude'])
                u.refresh_location_from_geocoder()
                u.save(update_fields=['region', 'district'])
                return u

            user = await update_loc()
            remove_kb = types.ReplyKeyboardRemove()
            if user.user_type == 'sotuvchi':
                await message.answer(get_text(user, 'LOCATION_SAVED'), reply_markup=remove_kb)
                await try_attach_seller_to_store(message, user, state)
            else:
                await message.answer(get_text(user, 'REGISTRATION_COMPLETE'), reply_markup=remove_kb)
                if state:
                    await state.clear()
                await show_main_menu(message, user)
                await message.answer(get_text(user, 'SEND_PROMO_CODE'))
            return
        # Текст «продолжить регистрацию» / «получить данные» / кнопка телефона — показываем следующий шаг
        continue_reg_texts = [
            'получить регистрационные данные', 'получить данные', 'продолжить регистрацию',
            'continue registration', 'ro\'yxatdan o\'tishni davom ettirish', 'registratsiya',
            'telefon raqamini yuborish', 'отправить номер', 'promokod kiritish', 'promokod',
        ]
        if message.text and any(t in message.text.lower() for t in continue_reg_texts):
            if not user.phone_number:
                await ask_phone(message, user, state)
            elif user.latitude is None or user.longitude is None:
                await ask_location(message, user, state)
            elif user.user_type == 'sotuvchi' and not user.owned_stores.filter(is_active=True).exists():
                await try_attach_seller_to_store(message, user, state)
            else:
                await message.answer(get_text(user, 'SEND_PROMO_CODE'))
                if state:
                    await state.set_state(RegistrationStates.waiting_for_promo_code)
            return

    # Tugma tekstlari to'plamlari
    all_balance_texts = [TRANSLATIONS['uz_latin']['MY_BALANCE'], TRANSLATIONS['ru']['MY_BALANCE']]
    all_gifts_texts = [TRANSLATIONS['uz_latin']['GIFTS'], TRANSLATIONS['ru']['GIFTS']]
    all_leaders_texts = [TRANSLATIONS['uz_latin']['TOP_LEADERS'], TRANSLATIONS['ru']['TOP_LEADERS']]
    all_leaders_month_texts = [TRANSLATIONS['uz_latin']['TOP_LEADERS_MONTH'], TRANSLATIONS['ru']['TOP_LEADERS_MONTH']]
    all_language_texts = [TRANSLATIONS['uz_latin']['LANGUAGE'], TRANSLATIONS['ru']['LANGUAGE']]
    all_promo_code_texts = [TRANSLATIONS['uz_latin']['ENTER_PROMO_CODE'], TRANSLATIONS['ru']['ENTER_PROMO_CODE']]

    # Sotuvchi tugmalari
    all_seller_balance_texts = [TRANSLATIONS['uz_latin']['SELLER_MY_BALANCE'], TRANSLATIONS['ru']['SELLER_MY_BALANCE']]
    all_seller_store_texts = [TRANSLATIONS['uz_latin']['SELLER_MY_STORE'], TRANSLATIONS['ru']['SELLER_MY_STORE']]
    all_seller_contact_texts = [TRANSLATIONS['uz_latin']['SELLER_CONTACT_ADMIN'], TRANSLATIONS['ru']['SELLER_CONTACT_ADMIN']]

    if message.text in all_seller_balance_texts:
        await show_seller_balance(message, user)
    elif message.text in all_seller_store_texts:
        await show_seller_store_info(message, user)
    elif message.text in all_seller_contact_texts:
        await show_admin_contact_for_seller(message, user)
    elif message.text in all_balance_texts:
        await show_balance(message, user)
    elif message.text in all_gifts_texts:
        web_app_url = get_web_app_url()
        inline_keyboard = None
        if web_app_url:
            try:
                inline_keyboard = types.InlineKeyboardMarkup(inline_keyboard=[[
                    types.InlineKeyboardButton(text=get_text(user, 'MY_GIFTS'), web_app=types.WebAppInfo(url=web_app_url))
                ]])
            except Exception as e:
                logger.warning(f"Web App inline button error: {e}")
        await message.answer(get_text(user, 'OPEN_WEB_APP'), reply_markup=inline_keyboard)
    elif message.text in all_leaders_texts:
        await show_leaders(message)
    elif message.text in all_leaders_month_texts:
        await show_leaders_month(message)
    elif message.text in all_language_texts:
        await show_language_selection(message)
    elif message.text in all_promo_code_texts:
        await message.answer(get_text(user, 'SEND_PROMO_CODE'))
        await state.set_state(RegistrationStates.waiting_for_promo_code)
    else:
        if message.text and len(message.text.strip()) > 0 and not message.contact and not message.location:
            qr_code_str = message.text.strip().upper()
            await handle_qr_code_scan(message, user, qr_code_str, state)
        else:
            await handle_unknown_message(message)


async def show_balance(message: Message, user: TelegramUser):
    """Santenik balansini ko'rsatadi."""
    @sync_to_async
    def get_actual_points():
        return user.calculate_points()

    actual_points = await get_actual_points()
    await message.answer(get_text(user, 'BALANCE_INFO', points=format_number(actual_points)))


async def show_seller_balance(message: Message, user: TelegramUser):
    """Sotuvchi balansini ko'rsatadi."""
    @sync_to_async
    def get_points():
        return TelegramUser.objects.get(telegram_id=message.from_user.id).calculate_points()

    points = await get_points()
    await message.answer(get_text(user, 'SELLER_BALANCE_INFO', points=format_number(points)))


async def show_seller_store_info(message: Message, user: TelegramUser):
    """Sotuvchi do'koni haqida ma'lumot ko'rsatadi."""
    @sync_to_async
    def get_store():
        return (
            TelegramUser.objects.get(telegram_id=message.from_user.id)
            .owned_stores.filter(is_active=True)
            .select_related('region')
            .first()
        )

    store = await get_store()
    if not store:
        await message.answer(get_text(user, 'SELLER_NO_STORE'))
        return

    @sync_to_async
    def get_store_stats():
        return store.total_qr_codes(), store.scanned_qr_codes()

    total, scanned = await get_store_stats()
    await message.answer(
        get_text(
            user, 'SELLER_STORE_INFO',
            name=store.name,
            address=store.address or '—',
            region=store.region.name_uz if store.region else '—',
            total=total,
            scanned=scanned,
            commission=store.commission_percent,
        ),
        parse_mode='HTML',
    )


async def show_admin_contact_for_seller(message: Message, user: TelegramUser):
    """Sotuvchi uchun admin kontaktini ko'rsatadi."""
    @sync_to_async
    def get_contact():
        from core.models import AdminContactSettings
        return AdminContactSettings.get_active_contact()

    contact = await get_contact()
    if contact:
        contact_url = contact.get_contact_url()
        text = f"📞 {contact_url or contact.contact_value}"
    else:
        text = get_text(user, 'SELLER_CONTACT_ADMIN')
    await message.answer(text)




async def show_gifts(message: Message, state: FSMContext):
    """Показывает список доступных подарков с фильтрацией по типу пользователя."""
    @sync_to_async
    def get_gifts_and_user():
        from django.db.models import Q
        user = TelegramUser.objects.get(telegram_id=message.from_user.id)
        # JIP: Sovg'alar faqat santenik uchun (sotuvchi sovg'a olmaydi)
        if user.user_type == 'sotuvchi':
            gifts = []
        else:
            gifts_query = Gift.objects.filter(is_active=True)
            gifts = list(gifts_query.order_by('order', 'points_cost'))
        return user, gifts
    
    user, gifts = await get_gifts_and_user()
    
    if not gifts:
        await message.answer(get_text(user, 'NO_GIFTS'))
        return
    
    text = get_text(user, 'GIFTS_LIST')
    buttons = []
    
    for gift in gifts:
        can_afford = "✅" if user.points >= gift.points_cost else "❌"
        # Получаем слово "ball" на нужном языке
        balance_text = get_text(user, 'BALANCE_INFO', points=1)
        if 'ball' in balance_text.lower():
            ball_word = 'ball'
        elif 'балл' in balance_text.lower():
            ball_word = 'балл'
        else:
            ball_word = 'ball'
        text += f"{can_afford} {gift.name} - {format_number(gift.points_cost)} {ball_word}\n"
        buttons.append([types.InlineKeyboardButton(
            text=f"{gift.name} ({format_number(gift.points_cost)} {ball_word})",
            callback_data=f"gift_{gift.id}"
        )])
    
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    await message.answer(text, reply_markup=keyboard)
    if state:
        await state.set_state(GiftRedemptionStates.selecting_gift)


@dp.callback_query(lambda c: c.data.startswith("gift_"))
async def process_gift_selection(callback: CallbackQuery, state: FSMContext):
    """Обрабатывает выбор подарка."""
    # Игнорируем callback от ботов
    if callback.from_user.is_bot:
        return
    
    gift_id = int(callback.data.split("_")[1])
    
    @sync_to_async
    def process_gift():
        try:
            gift = Gift.objects.get(id=gift_id, is_active=True)
            user = TelegramUser.objects.get(telegram_id=callback.from_user.id)
            
            # Проверяем, доступен ли подарок для типа пользователя
            if gift.user_type and gift.user_type != user.user_type:
                return {'error': 'not_available_for_user_type'}
            
            if user.points < gift.points_cost:
                return {'error': 'insufficient_points'}
            
            # Создаем запрос на получение подарка
            GiftRedemption.objects.create(
                user=user,
                gift=gift,
                status='pending'
            )
            
            # Инвалидируем кеш и пересчитываем баллы (GiftRedemption уже создан выше)
            user.invalidate_points_cache()
            remaining_points = user.calculate_points(force=True)
            
            return {
                'success': True,
                'gift_name': gift.name,
                'remaining_points': remaining_points
            }
        except Gift.DoesNotExist:
            return {'error': 'not_found'}
    
    try:
        result = await process_gift()
        
        @sync_to_async
        def get_user_for_callback():
            return TelegramUser.objects.get(telegram_id=callback.from_user.id)
        
        user = await get_user_for_callback()
        
        if result.get('error') == 'insufficient_points':
            await callback.answer(get_text(user, 'INSUFFICIENT_POINTS'), show_alert=True)
        elif result.get('error') == 'not_found':
            await callback.answer(get_text(user, 'GIFT_NOT_FOUND'), show_alert=True)
        elif result.get('error') == 'not_available_for_user_type':
            await callback.answer(get_text(user, 'GIFT_NOT_AVAILABLE_FOR_USER_TYPE'), show_alert=True)
        elif result.get('success'):
            await callback.answer(get_text(user, 'GIFT_REQUEST_SENT', gift_name=result['gift_name'], remaining_points=format_number(result['remaining_points'])).split('!')[0] + "!", show_alert=True)
            await callback.message.answer(get_text(user, 'GIFT_REQUEST_SENT',
                gift_name=result['gift_name'],
                remaining_points=format_number(result['remaining_points'])
            ))
            if state:
                await state.clear()
    except Exception as e:
        logger.error(f"Error processing gift selection: {e}")
        @sync_to_async
        def get_user_for_error():
            return TelegramUser.objects.get(telegram_id=callback.from_user.id)
        user = await get_user_for_error()
        await callback.answer(get_text(user, 'GIFT_REQUEST_ERROR'), show_alert=True)


async def show_leaders(message: Message):
    """Показывает ТОП лидеров по реальному балансу (earned - spent)."""
    @sync_to_async
    def get_leaders_and_user():
        user = TelegramUser.objects.get(telegram_id=message.from_user.id)
        user_type = user.user_type or 'santenik'
        leaders = list(
            TelegramUser.objects
            .filter(user_type=user_type, is_active=True, points__gt=0)
            .order_by('-points')[:10]
        )
        for u in leaders:
            u._leader_points = u.points
        return user, leaders
    
    user, leaders = await get_leaders_and_user()
    
    if not leaders:
        await message.answer(get_text(user, 'NO_LEADERS'))
        return
    
    text = get_text(user, 'TOP_LEADERS_TITLE')
    position = 1
    
    for leader in leaders:
        emoji = "🥇" if position == 1 else "🥈" if position == 2 else "🥉" if position == 3 else f"{position}"
        name = leader.first_name or get_text(user, 'USER')
        pts = getattr(leader, '_leader_points', leader.points)
        text += get_text(user, 'LEADER_ENTRY', position=emoji, name=name, points=pts)
        position += 1
    
    await message.answer(text)


async def show_leaders_month(message: Message):
    """Показывает ТОП лидеров за текущий месяц (earned this month - spent this month)."""
    @sync_to_async
    def get_leaders_and_user():
        from django.db.models import Sum
        from django.utils import timezone
        from datetime import timedelta

        user = TelegramUser.objects.get(telegram_id=message.from_user.id)
        user_type = user.user_type or 'santenik'

        now = timezone.localtime(timezone.now())
        month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        next_month = (month_start + timedelta(days=32)).replace(day=1)

        earned_rows = list(
            QRCode.objects
            .filter(
                is_scanned=True,
                is_deleted=False,
                scanned_by__user_type=user_type,
                scanned_by__is_active=True,
                scanned_by__isnull=False,
                scanned_at__gte=month_start,
                scanned_at__lt=next_month,
            )
            .values('scanned_by')
            .annotate(earned=Sum('points'))
        )
        if not earned_rows:
            return user, []

        user_ids = [r['scanned_by'] for r in earned_rows]
        earned_map = {r['scanned_by']: r['earned'] for r in earned_rows}

        spent_rows = list(
            GiftRedemption.objects
            .filter(
                user_id__in=user_ids,
                requested_at__gte=month_start,
                requested_at__lt=next_month,
            )
            .exclude(status__in=['rejected', 'cancelled_by_user', 'not_received'])
            .values('user_id')
            .annotate(spent=Sum('gift__points_cost'))
        )
        spent_map = {r['user_id']: r['spent'] for r in spent_rows}

        net_list = sorted(
            [(uid, max(0, earned_map[uid] - spent_map.get(uid, 0))) for uid in user_ids],
            key=lambda x: -x[1],
        )[:10]
        top_ids = [uid for uid, _ in net_list]
        net_map = {uid: net for uid, net in net_list}

        users_by_id = TelegramUser.objects.filter(id__in=top_ids).in_bulk(top_ids)
        leaders = [users_by_id.get(uid) for uid in top_ids if users_by_id.get(uid)]
        for u in leaders:
            u._leader_points = net_map.get(u.id, 0)
        return user, leaders

    user, leaders = await get_leaders_and_user()

    if not leaders:
        await message.answer(get_text(user, 'NO_LEADERS_MONTH'))
        return

    text = get_text(user, 'TOP_LEADERS_MONTH_TITLE')
    position = 1
    for leader in leaders:
        emoji = "🥇" if position == 1 else "🥈" if position == 2 else "🥉" if position == 3 else f"{position}"
        name = leader.first_name or get_text(user, 'USER')
        pts = getattr(leader, '_leader_points', leader.points)
        text += get_text(user, 'LEADER_ENTRY', position=emoji, name=name, points=pts)
        position += 1

    await message.answer(text)


async def show_language_selection(message: Message):
    """Показывает выбор языка."""
    @sync_to_async
    def get_user():
        return TelegramUser.objects.get(telegram_id=message.from_user.id)
    
    user = await get_user()
    
    # Используем фиксированные тексты для кнопок выбора языка
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(
            text=TRANSLATIONS['uz_latin']['UZBEK_LATIN'],
            callback_data='lang_uz_latin'
        )],
        [types.InlineKeyboardButton(
            text=TRANSLATIONS['uz_latin']['RUSSIAN'],
            callback_data='lang_ru'
        )],
    ])
    
    await message.answer(get_text(user, 'SELECT_LANGUAGE'), reply_markup=keyboard)


# Этот обработчик удален - теперь смена языка обрабатывается в process_language_selection выше


# ───────────────────────────── Выбор локации через виловят/туман ─────────────────────────────

async def send_set_location_request(chat_id: int, user: TelegramUser):
    """Отправляет пользователю приглашение выбрать виловят/туман через inline-клавиатуру."""
    language = user.language or 'uz_latin'
    keyboard = build_region_keyboard(language)
    prompt = get_text(user, 'LOCATION_REQUEST_PROMPT')
    await bot.send_message(chat_id=chat_id, text=prompt, reply_markup=keyboard)


@dp.callback_query(lambda c: c.data and c.data.startswith(CALLBACK_REGION_PREFIX))
async def process_setloc_region(callback: CallbackQuery):
    """Пользователь выбрал виловят — показываем туманы внутри него."""
    if callback.from_user.is_bot:
        return
    region_code = callback.data[len(CALLBACK_REGION_PREFIX):]

    @sync_to_async
    def get_user():
        return TelegramUser.objects.filter(telegram_id=callback.from_user.id).first()

    user = await get_user()
    if not user:
        await callback.answer()
        return

    language = user.language or 'uz_latin'
    region_info = UZBEKISTAN_REGIONS.get(region_code) or {}
    region_name = region_info.get('name_ru' if language == 'ru' else 'name_uz') or region_code

    text = get_text(user, 'LOCATION_CHOOSE_DISTRICT', region=region_name)
    back_label = get_text(user, 'LOCATION_BACK_BUTTON')
    keyboard = build_district_keyboard(region_code, language, back_label=back_label)

    try:
        await callback.message.edit_text(text, reply_markup=keyboard)
    except TelegramBadRequest:
        await callback.message.answer(text, reply_markup=keyboard)
    await callback.answer()


@dp.callback_query(lambda c: c.data == CALLBACK_SETLOC_BACK)
async def process_setloc_back(callback: CallbackQuery):
    """Возврат к списку виловятов."""
    if callback.from_user.is_bot:
        return

    @sync_to_async
    def get_user():
        return TelegramUser.objects.filter(telegram_id=callback.from_user.id).first()

    user = await get_user()
    if not user:
        await callback.answer()
        return

    language = user.language or 'uz_latin'
    text = get_text(user, 'LOCATION_CHOOSE_REGION')
    keyboard = build_region_keyboard(language)
    try:
        await callback.message.edit_text(text, reply_markup=keyboard)
    except TelegramBadRequest:
        await callback.message.answer(text, reply_markup=keyboard)
    await callback.answer()


@dp.callback_query(lambda c: c.data and c.data.startswith(CALLBACK_DISTRICT_PREFIX))
async def process_setloc_district(callback: CallbackQuery):
    """Пользователь выбрал туман — сохраняем регион/туман и координаты по умолчанию."""
    if callback.from_user.is_bot:
        return
    payload = callback.data[len(CALLBACK_DISTRICT_PREFIX):]
    parts = payload.split(':', 1)
    if len(parts) != 2:
        await callback.answer()
        return
    region_code, district_code = parts

    district_data = find_district_data(region_code, district_code)
    if not district_data:
        await callback.answer()
        return

    @sync_to_async
    def save_location():
        u = TelegramUser.objects.filter(telegram_id=callback.from_user.id).first()
        if not u:
            return None, None, None
        region = UzRegion.objects.filter(code=region_code).first()
        district = None
        if region:
            district = UzDistrict.objects.filter(region=region, code=district_code).first()
        u.region = region
        u.district = district
        u.latitude = district_data.get('lat')
        u.longitude = district_data.get('lon')
        u.save(update_fields=['region', 'district', 'latitude', 'longitude'])
        return u, region, district

    user, region, district = await save_location()
    if not user:
        await callback.answer()
        return

    language = user.language or 'uz_latin'
    region_name = (
        (region.name_ru if language == 'ru' else region.name_uz)
        if region else region_code
    )
    district_name = (
        (district.name_ru if language == 'ru' else district.name_uz)
        if district else district_code
    )
    text = get_text(user, 'LOCATION_SET_SUCCESS', region=region_name, district=district_name)
    try:
        await callback.message.edit_text(text)
    except TelegramBadRequest:
        await callback.message.answer(text)
    await callback.answer()


async def handle_unknown_message(message: Message):
    """Обработчик неизвестных сообщений."""
    @sync_to_async
    def get_user():
        return TelegramUser.objects.get(telegram_id=message.from_user.id)
    
    user = await get_user()
    await message.answer(get_text(user, 'UNKNOWN_COMMAND'))

