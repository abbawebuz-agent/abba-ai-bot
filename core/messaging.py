"""
Утилиты для отправки сообщений через Telegram бота.
"""
import asyncio
import logging
from typing import List, Optional
from aiogram import Bot
from aiogram.exceptions import (
    TelegramBadRequest,
    TelegramForbiddenError,
    TelegramAPIError,
    TelegramRetryAfter,
    TelegramNetworkError,
)
from aiogram.types import LinkPreviewOptions
from asgiref.sync import sync_to_async
from django.conf import settings
from django.utils import timezone
from .models import TelegramUser, BroadcastMessage
from .telegram_html import (
    sanitize_html_for_telegram,
    html_to_plain_text,
    visible_text_length,
)

logger = logging.getLogger(__name__)

# Лимиты Telegram API
# 30 сообщений в секунду для broadcast (фото тяжелее — берём с запасом)
TELEGRAM_BROADCAST_RATE_LIMIT = 20  # сообщений в секунду
TELEGRAM_MESSAGE_DELAY = 1.0 / TELEGRAM_BROADCAST_RATE_LIMIT  # 0.05 секунды между сообщениями

# Лимиты длины (Bot API)
TELEGRAM_CAPTION_LIMIT = 1024
TELEGRAM_TEXT_LIMIT = 4096

# Ошибки разметки: сообщение доставляем ещё раз, но уже без parse_mode
_PARSE_ERROR_MARKERS = (
    "can't parse entities",
    'unsupported start tag',
    'unmatched end tag',
    "can't find end tag",
    'unexpected end tag',
    'entity',
)

# Сколько раз повторяем при flood control / сетевой ошибке
_MAX_RETRIES = 3


async def send_message_to_user(
    bot: Bot,
    user: TelegramUser,
    text: str,
    parse_mode: Optional[str] = None,
    disable_notification: bool = False,
    photo_path: Optional[str] = None,
    disable_link_preview: bool = False,
    reply_markup=None,
) -> tuple[bool, Optional[str]]:
    """
    Отправляет сообщение конкретному пользователю.
    Поддерживает: текст с HTML-форматированием, ссылки, фото с подписью, inline-клавиатуру.

    Args:
        bot: Экземпляр бота
        user: Пользователь Telegram
        text: Текст сообщения (поддерживает HTML: <b>, <i>, <a href="">)
        parse_mode: Режим парсинга (HTML, Markdown)
        disable_notification: Отключить уведомление
        photo_path: Путь к файлу изображения (если указан — отправляется фото с caption)
        disable_link_preview: Не показывать превью по ссылкам в тексте (только для текстовых сообщений)
        reply_markup: Клавиатура (InlineKeyboardMarkup/ReplyKeyboardMarkup) для прикрепления к сообщению

    Returns:
        tuple: (успешно ли отправлено, сообщение об ошибке если есть)
    """
    is_html = bool(parse_mode) and parse_mode.upper() == 'HTML'
    html_text = sanitize_html_for_telegram(text) if (is_html and text) else (text or '')
    plain_text = html_to_plain_text(text) if (is_html and text) else (text or '')

    # Повтор после ошибки не должен слать фото второй раз
    state = {'photo_sent': False}

    async def _deliver(body: str, mode: Optional[str]):
        """Одна попытка доставки (фото с подписью / текст, с учётом лимитов длины)."""
        from aiogram.types import FSInputFile

        if photo_path:
            # Подпись к фото — максимум 1024 символа. Длинный текст шлём отдельным сообщением,
            # иначе Telegram отклоняет ВСЮ отправку ("caption is too long").
            body_len = visible_text_length(body) if mode else len(body)
            caption = body or None
            tail = None
            if caption and body_len > TELEGRAM_CAPTION_LIMIT:
                caption, tail = None, body
            if not state['photo_sent']:
                await bot.send_photo(
                    chat_id=user.telegram_id,
                    photo=FSInputFile(photo_path),
                    caption=caption,
                    parse_mode=mode if caption else None,
                    disable_notification=disable_notification,
                    reply_markup=reply_markup if not tail else None,
                )
                state['photo_sent'] = True
            if tail:
                await bot.send_message(
                    chat_id=user.telegram_id,
                    text=tail[:TELEGRAM_TEXT_LIMIT],
                    parse_mode=mode,
                    disable_notification=True,
                    reply_markup=reply_markup,
                )
            return

        send_kwargs = {
            'chat_id': user.telegram_id,
            'text': body[:TELEGRAM_TEXT_LIMIT],
            'parse_mode': mode,
            'disable_notification': disable_notification,
        }
        if disable_link_preview:
            send_kwargs['link_preview_options'] = LinkPreviewOptions(is_disabled=True)
        if reply_markup is not None:
            send_kwargs['reply_markup'] = reply_markup
        await bot.send_message(**send_kwargs)

    try:
        attempt = 0
        while True:
            attempt += 1
            try:
                await _deliver(html_text if is_html else (text or ''), parse_mode)
                break
            except TelegramRetryAfter as e:
                # Flood control — ждём столько, сколько просит Telegram, и повторяем
                if attempt > _MAX_RETRIES:
                    raise
                wait = getattr(e, 'retry_after', 5) or 5
                logger.warning(
                    "Flood control для %s: ждём %s с (попытка %s)",
                    user.telegram_id, wait, attempt,
                )
                await asyncio.sleep(wait + 1)
            except TelegramNetworkError as e:
                if attempt > _MAX_RETRIES:
                    raise
                logger.warning("Сетевая ошибка для %s: %s (попытка %s)", user.telegram_id, e, attempt)
                await asyncio.sleep(2 * attempt)
            except TelegramBadRequest as e:
                # Разметка сломана (Quill <span style>, <p>, &nbsp; и т.п.) —
                # доставляем то же самое, но простым текстом, чтобы рассылка не падала целиком
                err = str(e).lower()
                if is_html and any(marker in err for marker in _PARSE_ERROR_MARKERS):
                    logger.warning(
                        "HTML-разметка отклонена Telegram (%s) — отправляем как обычный текст", e,
                    )
                    await _deliver(plain_text, None)
                    break
                raise

        # Обновляем время последнего сообщения
        @sync_to_async
        def update_user_success():
            user.last_message_sent_at = timezone.now()
            user.is_active = True
            user.blocked_bot_at = None
            user.save(update_fields=['last_message_sent_at', 'is_active', 'blocked_bot_at'])
        
        await update_user_success()
        
        return True, None
        
    except TelegramForbiddenError as e:
        # Пользователь заблокировал бота
        logger.warning(f"Пользователь {user.telegram_id} заблокировал бота: {e}")
        
        @sync_to_async
        def update_user_blocked():
            user.is_active = False
            user.blocked_bot_at = timezone.now()
            user.save(update_fields=['is_active', 'blocked_bot_at'])
        
        await update_user_blocked()
        return False, "Пользователь заблокировал бота"
        
    except TelegramBadRequest as e:
        error_text = str(e).lower()
        # Деактивируем только если аккаунт удалён/не найден, но не при ошибках контента сообщения
        user_gone = any(phrase in error_text for phrase in (
            'chat not found', 'user is deactivated', 'bot was kicked',
            'have no rights', 'chat_id is empty',
        ))
        if user_gone:
            logger.warning(f"Пользователь {user.telegram_id} не доступен: {e}")

            @sync_to_async
            def update_user_inactive():
                user.is_active = False
                user.save(update_fields=['is_active'])

            await update_user_inactive()
        else:
            logger.warning(f"Ошибка контента при отправке пользователю {user.telegram_id}: {e}")
        return False, f"Ошибка запроса: {str(e)}"
        
    except TelegramAPIError as e:
        # Другие ошибки API
        logger.error(f"Ошибка Telegram API для пользователя {user.telegram_id}: {e}")
        return False, f"Ошибка API: {str(e)}"
        
    except Exception as e:
        # Неожиданные ошибки
        logger.error(f"Неожиданная ошибка при отправке пользователю {user.telegram_id}: {e}")
        return False, f"Неожиданная ошибка: {str(e)}"


async def send_broadcast_message(
    broadcast: BroadcastMessage,
    bot: Bot,
    user_type_filter: Optional[str] = None
) -> dict:
    """
    Отправляет массовое сообщение всем активным пользователям.
    
    Args:
        broadcast: Объект рассылки
        bot: Экземпляр бота
        user_type_filter: Фильтр по типу пользователя (опционально, если не указан, используется из broadcast)
    
    Returns:
        dict: Статистика отправки
    """
    # Получаем активных пользователей
    @sync_to_async
    def get_users():
        users_query = TelegramUser.objects.filter(is_active=True)
        
        # Фильтр по типу пользователя
        filter_user_type = user_type_filter or broadcast.user_type_filter
        if filter_user_type:
            users_query = users_query.filter(user_type=filter_user_type)
        
        # Filtr do'kon bo'yicha: do'kon egasi + shu do'kondan QR skan qilgan santenik
        if broadcast.store_filter_id:
            from django.db.models import Q as _Q
            store_owner_ids = list(
                broadcast.store_filter.owner_id and [broadcast.store_filter.owner_id] or []
            )
            santenik_ids = list(
                users_query.filter(
                    user_type='santenik',
                    scanned_qrcodes__store_id=broadcast.store_filter_id,
                    scanned_qrcodes__is_scanned=True,
                    scanned_qrcodes__is_deleted=False,
                ).values_list('id', flat=True).distinct()
            )
            allowed_ids = set(store_owner_ids) | set(santenik_ids)
            users_query = users_query.filter(id__in=allowed_ids)

        # Фильтр по языку
        if broadcast.language_filter:
            users_query = users_query.filter(language=broadcast.language_filter)
        
        # Фильтр по региону
        if broadcast.region_filter:
            from core.regions import get_user_region_code

            # Получаем всех пользователей с геолокацией
            users_with_location = list(users_query.filter(
                latitude__isnull=False,
                longitude__isnull=False
            ))

            # Фильтруем по выбранному региону
            filtered_user_ids = []
            for user in users_with_location:
                user_region = get_user_region_code(user)
                if user_region == broadcast.region_filter:
                    filtered_user_ids.append(user.id)
            
            # Применяем фильтр по ID
            if filtered_user_ids:
                users_query = users_query.filter(id__in=filtered_user_ids)
            else:
                # Если никого не найдено, возвращаем пустой queryset
                users_query = users_query.none()
        
        return list(users_query)
    
    users = await get_users()
    total_users = len(users)
    
    # Обновляем статистику рассылки
    @sync_to_async
    def update_broadcast_start():
        broadcast.total_users = total_users
        broadcast.status = 'sending'
        broadcast.started_at = timezone.now()
        broadcast.save(update_fields=['total_users', 'status', 'started_at'])
    
    await update_broadcast_start()
    
    sent_count = 0
    failed_count = 0
    
    logger.info(f"Начало рассылки '{broadcast.title}' для {total_users} пользователей")
    
    # Путь к изображению (если есть)
    photo_path = None
    if broadcast.image:
        try:
            photo_path = broadcast.image.path
        except (ValueError, OSError):
            pass

    # Отправляем сообщения с учетом лимитов
    for i, user in enumerate(users):
        try:
            success, error = await send_message_to_user(
                bot=bot,
                user=user,
                text=broadcast.message_text,
                parse_mode='HTML',
                photo_path=photo_path,
                disable_link_preview=True,
            )
            
            if success:
                sent_count += 1
            else:
                failed_count += 1
                logger.warning(f"Не удалось отправить пользователю {user.telegram_id}: {error}")
            
            # Обновляем статистику каждые 10 сообщений
            if (i + 1) % 10 == 0:
                @sync_to_async
                def update_broadcast_progress():
                    broadcast.sent_count = sent_count
                    broadcast.failed_count = failed_count
                    broadcast.save(update_fields=['sent_count', 'failed_count'])
                
                await update_broadcast_progress()
            
            # Соблюдаем лимит Telegram API (30 сообщений в секунду)
            # Добавляем небольшую задержку между сообщениями
            if i < total_users - 1:  # Не ждем после последнего сообщения
                await asyncio.sleep(TELEGRAM_MESSAGE_DELAY)
                
        except Exception as e:
            logger.error(f"Критическая ошибка при отправке пользователю {user.telegram_id}: {e}")
            failed_count += 1
            # Помечаем пользователя как неактивного при критической ошибке
            @sync_to_async
            def mark_user_inactive():
                user.is_active = False
                user.save(update_fields=['is_active'])
            
            await mark_user_inactive()
    
    # Завершаем рассылку
    @sync_to_async
    def update_broadcast_complete():
        broadcast.sent_count = sent_count
        broadcast.failed_count = failed_count
        broadcast.status = 'completed'
        broadcast.completed_at = timezone.now()
        broadcast.save(update_fields=['sent_count', 'failed_count', 'status', 'completed_at'])
    
    await update_broadcast_complete()
    
    logger.info(
        f"Рассылка '{broadcast.title}' завершена: "
        f"отправлено {sent_count}, ошибок {failed_count} из {total_users}"
    )
    
    return {
        'total': total_users,
        'sent': sent_count,
        'failed': failed_count
    }


async def send_personal_message(
    bot: Bot,
    telegram_id: int,
    text: str,
    parse_mode: Optional[str] = None
) -> tuple[bool, Optional[str]]:
    """
    Отправляет персональное сообщение конкретному пользователю.
    
    Args:
        bot: Экземпляр бота
        telegram_id: Telegram ID пользователя
        text: Текст сообщения
        parse_mode: Режим парсинга (HTML, Markdown)
    
    Returns:
        tuple: (успешно ли отправлено, сообщение об ошибке если есть)
    """
    @sync_to_async
    def get_user():
        try:
            return TelegramUser.objects.get(telegram_id=telegram_id)
        except TelegramUser.DoesNotExist:
            return None
    
    user = await get_user()
    if user is None:
        return False, "Пользователь не найден"
    
    return await send_message_to_user(
        bot=bot,
        user=user,
        text=text,
        parse_mode=parse_mode
    )

