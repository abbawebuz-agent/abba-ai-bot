"""
Views for Telegram Web App.
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from django.conf import settings
from django.utils import translation
from django.db import models
from functools import wraps
from .models import TelegramUser, Gift, GiftRedemption, QRCode, Promotion, PrivacyPolicy, AdminContactSettings, LiveStream, Store, QRCodeBatch, SellerPointsTransaction
from .serializers import GiftSerializer, GiftRedemptionSerializer
from django.utils import timezone


def no_cache_response(func):
    """Декоратор для добавления заголовков отключения кеша к ответам API."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        response = func(*args, **kwargs)
        if isinstance(response, Response):
            response['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0, private'
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'
            response['X-Accel-Expires'] = '0'
            # Удаляем заголовки кеширования, если они есть
            if 'ETag' in response:
                del response['ETag']
            if 'Last-Modified' in response:
                del response['Last-Modified']
        return response
    return wrapper


def webapp_view(request):
    """Главная страница веб-приложения."""
    # Определяем язык пользователя из initData или параметра
    user_language = 'uz_latin'  # По умолчанию
    
    # Пытаемся получить язык из Telegram initData (передается через JavaScript)
    # Telegram Web App передает initData через window.Telegram.WebApp.initData
    # Мы будем получать язык через JavaScript и передавать в контекст
    
    # Если передан telegram_id в GET параметрах, получаем язык из БД
    telegram_id = request.GET.get('telegram_id') or request.GET.get('tg_id')
    if telegram_id:
        try:
            user = TelegramUser.objects.get(telegram_id=int(telegram_id))
            user_language = user.language
        except (TelegramUser.DoesNotExist, ValueError):
            pass
    
    # Версия для cache busting (изменяйте при обновлении CSS/JS)
    import time
    app_version = str(int(time.time()))  # Используем timestamp для гарантии обновления
    
    # Не используем Django i18n для кастомных языков, используем наш template tag
    # Просто передаем язык в контекст для использования в шаблоне
    context = {
        'user_language': user_language,
        'TELEGRAM_BOT_USERNAME': settings.TELEGRAM_BOT_USERNAME or '',
        'TELEGRAM_BOT_ADMIN_USERNAME': settings.TELEGRAM_BOT_ADMIN_USERNAME or '',
        'app_version': app_version,
    }
    
    response = render(request, 'webapp/index_v5.html', context)
    
    # Добавляем заголовки для отключения кеширования
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0, private'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    response['X-Accel-Expires'] = '0'  # Для nginx
    # Удаляем заголовки кеширования, если они есть
    if 'ETag' in response:
        del response['ETag']
    if 'Last-Modified' in response:
        del response['Last-Modified']
    
    return response


@api_view(['GET'])
@permission_classes([AllowAny])
@no_cache_response
def get_user_data(request):
    """Получает данные пользователя по telegram_id из initData."""
    telegram_id = request.GET.get('telegram_id')
    
    if not telegram_id:
        return Response(
            {'error': 'telegram_id is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        user = TelegramUser.objects.get(telegram_id=int(telegram_id))

        is_registered = bool(
            user.language and
            user.privacy_accepted and
            user.phone_number and
            user.region_id
        )

        serializer = {
            'id': user.id,
            'telegram_id': user.telegram_id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'username': user.username,
            'phone_number': user.phone_number,
            'points': user.calculate_points(),
            'qr_scan_count': QRCode.objects.filter(scanned_by=user, is_scanned=True, is_deleted=False).count(),
            'user_type': user.user_type,
            'language': user.language,
            'is_registered': is_registered,
        }

        # Месяц/шансы выносим в отдельный эндпоинт webapp/monthly-stats/,
        # чтобы не нагружать главную страницу подсчётом шансов.
        return Response(serializer)
    except TelegramUser.DoesNotExist:
        return Response(
            {'error': 'User not found', 'is_registered': False},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['GET'])
@permission_classes([AllowAny])
@no_cache_response
def get_translations(request):
    """Получает переводы для Web App на указанном языке."""
    from bot.translations import TRANSLATIONS
    
    language = request.GET.get('lang', 'uz_latin')
    
    # Получаем переводы для указанного языка
    translations = TRANSLATIONS.get(language, TRANSLATIONS.get('uz_latin', {}))
    
    return Response(translations)


@api_view(['GET'])
@permission_classes([AllowAny])
@no_cache_response
def get_gifts(request):
    """Получает список активных подарков."""
    try:
        telegram_id = request.GET.get('telegram_id')
        language = 'uz_latin'

        gifts_query = Gift.objects.filter(is_active=True)

        if telegram_id:
            try:
                user = TelegramUser.objects.get(telegram_id=int(telegram_id))
                language = user.language or 'uz_latin'
            except TelegramUser.DoesNotExist:
                pass

        gifts = gifts_query.order_by('order', 'points_cost')
        serializer = GiftSerializer(
            gifts,
            many=True,
            context={'request': request, 'language': language},
        )
        return Response(serializer.data)
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([AllowAny])
@no_cache_response
def get_user_redemptions(request):
    """Получает список запросов на подарки пользователя."""
    telegram_id = request.GET.get('telegram_id')
    
    if not telegram_id:
        return Response(
            {'error': 'telegram_id is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        user = TelegramUser.objects.get(telegram_id=int(telegram_id))
        redemptions = GiftRedemption.objects.filter(user=user).order_by('-requested_at')
        serializer = GiftRedemptionSerializer(redemptions, many=True, context={'request': request})
        return Response(serializer.data)
    except TelegramUser.DoesNotExist:
        return Response(
            {'error': 'User not found'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['POST'])
@permission_classes([AllowAny])
@no_cache_response
def request_gift(request):
    """Создает запрос на получение подарка."""
    telegram_id = request.data.get('telegram_id')
    gift_id = request.data.get('gift_id')
    
    if not telegram_id or not gift_id:
        return Response(
            {'error': 'telegram_id and gift_id are required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        user = TelegramUser.objects.get(telegram_id=int(telegram_id))
        gift = Gift.objects.get(id=gift_id, is_active=True)
        

        
        # Проверяем баланс (вычисляемый, без кеша для точности)
        current_points = user.calculate_points(force=True)
        if current_points < gift.points_cost:
            from bot.translations import get_text
            error_message = get_text(user, 'INSUFFICIENT_POINTS')
            return Response(
                {'error': error_message},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Создаем запрос
        redemption = GiftRedemption.objects.create(
            user=user,
            gift=gift,
            status='pending'
        )

        # Инвалидируем кеш и пересчитываем баллы
        user.invalidate_points_cache()
        remaining_points = user.calculate_points(force=True)

        # Уведомление пользователю в Telegram о принятой заявке
        try:
            from bot.translations import get_text
            gift_name = gift.get_name(user.language or 'uz_latin')
            message_text = get_text(
                user,
                'GIFT_REQUEST_SENT',
                gift_name=gift_name,
                remaining_points=remaining_points,
            )
            _tg_api('sendMessage', {
                'chat_id': user.telegram_id,
                'text': message_text,
            })
        except Exception as notify_err:
            import logging
            logging.getLogger(__name__).warning(
                "Failed to send gift-request notification to %s: %s",
                user.telegram_id, notify_err,
            )

        serializer = GiftRedemptionSerializer(redemption, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    except TelegramUser.DoesNotExist:
        return Response(
            {'error': 'User not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Gift.DoesNotExist:
        return Response(
            {'error': 'Gift not found'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['POST'])
@permission_classes([AllowAny])
@no_cache_response
def cancel_order(request):
    """Отмена заказа пользователем (в течение 1 часа после создания)."""
    redemption_id = request.data.get('redemption_id')
    telegram_id = request.data.get('telegram_id')
    
    if not redemption_id or not telegram_id:
        return Response(
            {'error': 'redemption_id and telegram_id are required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        user = TelegramUser.objects.get(telegram_id=int(telegram_id))
        redemption = GiftRedemption.objects.get(id=redemption_id, user=user)
        
        # Проверяем статус - можно отменить только pending
        if redemption.status != 'pending':
            return Response(
                {'error': 'Можно отменить только заказы в статусе ожидания'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Проверяем 1-часовое окно
        time_diff = timezone.now() - redemption.requested_at
        if time_diff.total_seconds() > 3600:  # 1 час = 3600 секунд
            from bot.translations import get_text
            return Response(
                {'error': get_text(user, 'WEBAPP_CANCEL_ORDER_EXPIRED')},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Отменяем заказ
        redemption.status = 'cancelled_by_user'
        redemption.save(update_fields=['status'])
        
        # Инвалидируем кеш и пересчитываем баллы (баллы возвращаются автоматически)
        user.invalidate_points_cache()
        user.calculate_points(force=True)
        
        serializer = GiftRedemptionSerializer(redemption, context={'request': request})
        return Response({
            'success': True,
            'redemption': serializer.data,
            'new_points': user.calculate_points()
        })
        
    except TelegramUser.DoesNotExist:
        return Response(
            {'error': 'User not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    except GiftRedemption.DoesNotExist:
        return Response(
            {'error': 'Redemption not found'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['POST'])
@permission_classes([AllowAny])
@no_cache_response
def confirm_delivery(request):
    """Подтверждает получение заказа или оставляет комментарий."""
    redemption_id = request.data.get('redemption_id')
    confirmed = request.data.get('confirmed', False)
    comment = request.data.get('comment', '')
    
    if not redemption_id:
        return Response(
            {'error': 'redemption_id is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        redemption = GiftRedemption.objects.get(id=redemption_id)
        
        redemption.user_confirmed = confirmed
        redemption.user_comment = comment
        update_fields = ['user_confirmed', 'user_comment']

        if confirmed:
            # Пользователь подтвердил получение подарка
            redemption.confirmed_at = timezone.now()
            redemption.status = 'completed'
            update_fields.extend(['confirmed_at', 'status'])
        else:
            # Пользователь указал, что подарок не получил
            redemption.confirmed_at = timezone.now()
            redemption.status = 'not_received'
            update_fields.extend(['confirmed_at', 'status'])

        redemption.save(update_fields=update_fields)
        
        serializer = GiftRedemptionSerializer(redemption, context={'request': request})
        return Response(serializer.data)
        
    except GiftRedemption.DoesNotExist:
        return Response(
            {'error': 'Redemption not found'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['GET'])
@permission_classes([AllowAny])
@no_cache_response
def get_qr_history(request):
    """
    История отсканированных QR-кодов пользователя.
    ?month=current — фильтр по текущему месяцу (для UI «шансы этого месяца»).
    Каждый элемент включает monthly_order (билет №) если у QR есть билет.
    """
    telegram_id = request.GET.get('telegram_id')
    month_filter = (request.GET.get('month') or '').strip().lower()

    if not telegram_id:
        return Response(
            {'error': 'telegram_id is required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        user = TelegramUser.objects.get(telegram_id=int(telegram_id))
        qr_codes = QRCode.objects.filter(
            scanned_by=user,
            is_scanned=True,
            is_deleted=False,
        ).order_by('-scanned_at')

        if month_filter == 'current':
            from django.utils import timezone
            now = timezone.localtime(timezone.now())
            qr_codes = qr_codes.filter(scanned_at__year=now.year, scanned_at__month=now.month)

        history = []
        for qr in qr_codes:
            history.append({
                'id': qr.id,
                'code': qr.code,
                'points': qr.points,
                'scanned_at': qr.scanned_at.strftime('%d.%m.%Y') if qr.scanned_at else None,
                'store_name': qr.store.name if qr.store_id else None,
            })

        return Response(history)
    except TelegramUser.DoesNotExist:
        return Response(
            {'error': 'User not found'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['GET'])
@permission_classes([AllowAny])
@no_cache_response
def get_promotions(request):
    """Получает список активных акций для слайдера."""
    try:
        promotions = Promotion.objects.filter(is_active=True).order_by('order', '-created_at')
        
        promotions_data = []
        for promotion in promotions:
            promotions_data.append({
                'id': promotion.id,
                'title': promotion.title,
                'image': request.build_absolute_uri(promotion.image.url) if promotion.image else None,
                'date': promotion.date.strftime('%d.%m.%Y') if promotion.date else None,
            })
        
        return Response(promotions_data)
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([AllowAny])
@no_cache_response
def get_promotion_detail(request, promotion_id):
    """Получает детальную информацию об акции."""
    try:
        promotion = Promotion.objects.get(id=promotion_id, is_active=True)
        
        promotion_data = {
            'id': promotion.id,
            'title': promotion.title,
            'image': request.build_absolute_uri(promotion.image.url) if promotion.image else None,
            'date': promotion.date.strftime('%d.%m.%Y') if promotion.date else None,
        }
        
        return Response(promotion_data)
    except Promotion.DoesNotExist:
        return Response(
            {'error': 'Promotion not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([AllowAny])
@no_cache_response
def get_privacy_policy(request):
    """Получает политику конфиденциальности на указанном языке."""
    language = request.GET.get('lang', 'uz_latin')
    
    try:
        policy = PrivacyPolicy.objects.filter(is_active=True).first()
        
        if not policy:
            return Response(
                {'error': 'Privacy policy not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Выбираем PDF в зависимости от языка
        if language == 'uz_latin':
            pdf_file = policy.pdf_uz_latin
        elif language == 'ru':
            pdf_file = policy.pdf_ru
        else:
            pdf_file = policy.pdf_uz_latin
        
        # Формируем URL для PDF файла, если он существует
        pdf_url = None
        if pdf_file:
            pdf_url = request.build_absolute_uri(pdf_file.url)
        
        return Response({
            'pdf_url': pdf_url,
            'updated_at': policy.updated_at.strftime('%d.%m.%Y %H:%M') if policy.updated_at else None
        })
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([AllowAny])
@no_cache_response
def get_admin_contact(request):
    """Получает настройки контакта администратора.

    Возвращает массив `contacts` (все активные контакты) + первый контакт
    в верхнеуровневых полях `contact_type/value/url` для обратной совместимости.
    """
    try:
        active_contacts = list(AdminContactSettings.get_active_contacts())

        if not active_contacts:
            return Response({
                'contacts': [],
                'contact_type': None,
                'contact_value': None,
                'contact_url': None,
            })

        contacts = [
            {
                'contact_type': c.contact_type,
                'contact_value': c.contact_value,
                'contact_url': c.get_contact_url(),
            }
            for c in active_contacts
        ]

        first = contacts[0]
        return Response({
            'contacts': contacts,
            'contact_type': first['contact_type'],
            'contact_value': first['contact_value'],
            'contact_url': first['contact_url'],
        })
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([AllowAny])
@no_cache_response
def update_user_language(request):
    """Обновляет язык пользователя."""
    telegram_id = request.data.get('telegram_id')
    language = request.data.get('language')
    
    if not telegram_id or not language:
        return Response(
            {'error': 'telegram_id and language are required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if language not in ['uz_latin', 'ru']:
        return Response(
            {'error': 'Invalid language'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        user = TelegramUser.objects.get(telegram_id=int(telegram_id))
        user.language = language
        user.save(update_fields=['language'])
        
        return Response({
            'success': True,
            'language': user.language
        })
    except TelegramUser.DoesNotExist:
        return Response(
            {'error': 'User not found'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['POST'])
@permission_classes([AllowAny])
@no_cache_response
def register_qr_code(request):
    """Регистрирует QR-код для пользователя."""
    from django.utils import timezone
    from django.conf import settings
    from core.models import QRCode, QRCodeScanAttempt
    
    telegram_id = request.data.get('telegram_id')
    qr_code_str = request.data.get('qr_code')
    
    if not telegram_id or not qr_code_str:
        return Response(
            {'error': 'telegram_id and qr_code are required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        user = TelegramUser.objects.get(telegram_id=int(telegram_id))
    except TelegramUser.DoesNotExist:
        return Response(
            {'error': 'User not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    from django.db import transaction
    from bot.translations import get_text
    
    try:
        # Сначала проверяем, не заблокирован ли пользователь по промокодам
        blocked, block_type, blocked_until = user.is_promo_code_blocked()
        if blocked:
            # Сообщение в зависимости от уровня блокировки
            if block_type == 'permanent':
                error_message = get_text(user, 'PROMO_BLOCKED_PERMANENT')
            else:
                error_message = get_text(user, 'PROMO_BLOCKED_1_DAY')
            return Response(
                {'error': error_message, 'error_code': 'promo_blocked'},
                status=status.HTTP_400_BAD_REQUEST
            )

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
                    # QR-код не найден — регистрируем неверную попытку
                    user.register_invalid_promo_attempt(source='webapp', raw_code=qr_code_str)
                    error_message = get_text(user, 'QR_NOT_FOUND')
                    return Response(
                        {'error': error_message, 'error_code': 'not_found'},
                        status=status.HTTP_404_NOT_FOUND
                    )
            
            # Проверяем, не был ли уже отсканирован
            if qr_code.is_scanned:
                # Создаем запись о неудачной попытке
                QRCodeScanAttempt.objects.create(
                    user=user,
                    qr_code=qr_code,
                    is_successful=False
                )
                user.register_invalid_promo_attempt(source='webapp', raw_code=qr_code_str)
                error_message = get_text(user, 'QR_ALREADY_SCANNED')
                return Response(
                    {'error': error_message, 'error_code': 'already_scanned'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # JIP: Faqat santenik QR kodni skanlashi mumkin
            if user.user_type != 'santenik':
                QRCodeScanAttempt.objects.create(user=user, qr_code=qr_code, is_successful=False)
                user.register_invalid_promo_attempt(source='webapp', raw_code=qr_code_str)
                error_message = get_text(user, 'QR_WRONG_TYPE')
                return Response(
                    {'error': error_message, 'error_code': 'wrong_type'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Отмечаем QR-код как отсканированный
            qr_code.is_scanned = True
            qr_code.scanned_at = timezone.now()
            qr_code.scanned_by = user
            qr_code.save(update_fields=['is_scanned', 'scanned_at', 'scanned_by'])

            # Monthly promo ticket olib tashlandi (user talab).

            # Создаем запись об успешной попытке
            QRCodeScanAttempt.objects.create(
                user=user,
                qr_code=qr_code,
                is_successful=True
            )
            # Фиксируем успешный промокод (сброс последовательности ошибок)
            user.register_successful_promo(raw_code=qr_code_str, source='webapp')
            
            # Инвалидируем кеш и пересчитываем баллы
            user.invalidate_points_cache()
            total_points = user.calculate_points(force=True)
            
            success_message = get_text(user, 'QR_ACTIVATED',
                points=qr_code.points,
                total_points=total_points
            )
            
            return Response({
                'success': True,
                'message': success_message,
                'points': qr_code.points,
                'total_points': total_points
            })
        
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error processing QR code scan in webapp: {e}")
        
        error_message = get_text(user, 'QR_ERROR')
        return Response(
            {'error': error_message},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# ──────────────────────────────────────────────────────────────────────────────
# Helpers for sending Telegram Bot API messages without aiogram
# ──────────────────────────────────────────────────────────────────────────────

def _tg_api(method: str, payload: dict) -> bool:
    """Sends a request to the Telegram Bot API. Returns True on success."""
    import json
    import urllib.request
    import urllib.error
    import logging

    logger = logging.getLogger(__name__)
    token = settings.TELEGRAM_BOT_TOKEN
    if not token:
        return False

    # Telegram sendMessage: text must be non-empty and at most 4096 characters
    if method == 'sendMessage':
        text = payload.get('text')
        if not (text and str(text).strip()):
            logger.warning("[_tg_api] sendMessage skipped: empty text")
            return False
        payload = {**payload, 'text': str(text).strip()[:4096]}

    url = f"https://api.telegram.org/bot{token}/{method}"
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(
        url, data=data,
        headers={'Content-Type': 'application/json'},
        method='POST',
    )
    try:
        with urllib.request.urlopen(req, timeout=10):
            return True
    except urllib.error.HTTPError as e:
        try:
            body = e.read().decode('utf-8', errors='replace')
            desc = body
            try:
                doc = json.loads(body)
                desc = doc.get('description', body)
            except Exception:
                pass

            desc_lower = str(desc).lower()
            is_forbidden = e.code == 403
            is_chat_not_found = e.code == 400 and 'chat not found' in desc_lower

            # 403 = пользователь заблокировал бота — ожидаемо, не ошибка
            # 400 + "chat not found" = пользователь ещё не открыл чат с ботом — тоже ожидаемо
            if is_forbidden or is_chat_not_found:
                reason = (
                    "user likely blocked the bot"
                    if is_forbidden
                    else "chat not found (user never started bot)"
                )
                logger.warning(
                    "[_tg_api] %s HTTP %s (%s): %s",
                    method, e.code, reason, desc,
                )
            else:
                logger.error(
                    "[_tg_api] %s failed: HTTP %s - %s",
                    method, e.code, desc,
                    extra={'telegram_response': body[:500]},
                )
        except Exception:
            if e.code == 403:
                logger.warning("[_tg_api] %s HTTP 403 (user likely blocked the bot)", method)
            elif e.code == 400:
                logger.warning("[_tg_api] %s HTTP 400 (chat not found or bad request)", method)
            else:
                logger.error("[_tg_api] %s failed: HTTP %s - %s", method, e.code, e)
        return False
    except Exception as exc:
        logger.error(f"[_tg_api] {method} failed: {exc}")
        return False


def _resend_step_for_user(user: TelegramUser) -> str:
    """
    Determines the current registration step and sends the appropriate
    Telegram message/keyboard to the user. Returns the step name.
    """
    from bot.translations import get_text

    def _btn(key, fallback: str = "…"):
        """Button label: never empty (Telegram requirement)."""
        s = get_text(user, key) if isinstance(key, str) else key
        return (s or fallback).strip() or fallback

    chat_id = user.telegram_id

    # ── Step 1: Language ────────────────────────────────────────────────────
    if not user.language:
        _tg_api('sendMessage', {
            'chat_id': chat_id,
            'text': (
                "Assalomu alaykum!\n«JIP» dasturiga xush kelibsiz.\n"
                "Iltimos, qulay bo'lgan tilni tanlang:\n\n"
                "Добрый день!\nДобро пожаловать в программу «JIP».\n"
                "Пожалуйста, выберите удобный для вас язык:"
            ),
            'reply_markup': {
                'inline_keyboard': [
                    [{'text': "🇺🇿 O'zbekcha", 'callback_data': 'lang_uz_latin'}],
                    [{'text': "🇷🇺 Русский",    'callback_data': 'lang_ru'}],
                ],
            },
        })
        return 'language'

    # ── Step 2: Name ────────────────────────────────────────────────────────
    if not user.first_name:
        _tg_api('sendMessage', {
            'chat_id': chat_id,
            'text': get_text(user, 'ASK_NAME'),
        })
        return 'name'

    # ── Step 3: User type ───────────────────────────────────────────────────
    if not user.user_type:
        _tg_api('sendMessage', {
            'chat_id': chat_id,
            'text': get_text(user, 'SELECT_USER_TYPE'),
            'reply_markup': {
                'inline_keyboard': [
                    [{'text': _btn('USER_TYPE_ELECTRICIAN'), 'callback_data': 'user_type_electrician'}],
                    [{'text': _btn('USER_TYPE_SELLER'), 'callback_data': 'user_type_seller'}],
                ],
            },
        })
        return 'user_type'

    # ── Step 4: Privacy ─────────────────────────────────────────────────────
    if not user.privacy_accepted:
        _tg_api('sendMessage', {
            'chat_id': chat_id,
            'text': get_text(user, 'PRIVACY_POLICY_TEXT'),
            'reply_markup': {
                'inline_keyboard': [
                    [{'text': _btn('ACCEPT_PRIVACY'), 'callback_data': 'privacy_accept'}],
                    [{'text': _btn('DECLINE_PRIVACY'), 'callback_data': 'privacy_decline'}],
                ],
            },
        })
        return 'privacy'

    # ── Step 5: Phone ───────────────────────────────────────────────────────
    if not user.phone_number:
        _tg_api('sendMessage', {
            'chat_id': chat_id,
            'text': get_text(user, 'SEND_PHONE'),
            'reply_markup': {
                'keyboard': [[{'text': _btn('SEND_PHONE_BUTTON', '📱'), 'request_contact': True}]],
                'resize_keyboard': True,
                'one_time_keyboard': True,
            },
        })
        return 'phone'

    # ── Step 6: Location ────────────────────────────────────────────────────
    if user.latitude is None or user.longitude is None:
        location_text = get_text(user, 'SEND_LOCATION') or ''
        btn_text = ("📍 " + location_text.replace('📍 ', '').strip()).strip() or "📍"
        _tg_api('sendMessage', {
            'chat_id': chat_id,
            'text': location_text or _btn('SEND_LOCATION', 'Location'),
            'reply_markup': {
                'keyboard': [[{'text': btn_text, 'request_location': True}]],
                'resize_keyboard': True,
                'one_time_keyboard': True,
            },
        })
        return 'location'

    # ── Step 7: Promo code ──────────────────────────────────────────────────
    _tg_api('sendMessage', {
        'chat_id': chat_id,
        'text': get_text(user, 'SEND_PROMO_CODE'),
        'reply_markup': {'remove_keyboard': True},
    })
    return 'promo_code'


@api_view(['POST'])
@permission_classes([AllowAny])
def resend_registration_step(request):
    """
    Определяет текущий шаг регистрации пользователя и отправляет ему
    напоминание через Telegram Bot API.
    """
    telegram_id = request.data.get('telegram_id')
    if not telegram_id:
        return Response({'error': 'telegram_id is required'},
                        status=status.HTTP_400_BAD_REQUEST)

    try:
        user = TelegramUser.objects.get(telegram_id=int(telegram_id))
    except TelegramUser.DoesNotExist:
        # Пользователь совсем новый — отправляем стартовое сообщение
        _tg_api('sendMessage', {
            'chat_id': int(telegram_id),
            'text': (
                "Assalomu alaykum!\n«JIP» dasturiga xush kelibsiz.\n"
                "Iltimos, qulay bo'lgan tilni tanlang:\n\n"
                "Добрый день!\nДобро пожаловать в программу «JIP».\n"
                "Пожалуйста, выберите удобный для вас язык:"
            ),
            'reply_markup': {
                'inline_keyboard': [
                    [{'text': "🇺🇿 O'zbekcha", 'callback_data': 'lang_uz_latin'}],
                    [{'text': "🇷🇺 Русский",    'callback_data': 'lang_ru'}],
                ],
            },
        })
        return Response({'success': True, 'step': 'language'})

    step = _resend_step_for_user(user)
    return Response({'success': True, 'step': step})


def _live_stream_language(request):
    telegram_id = request.GET.get('telegram_id')
    if telegram_id:
        try:
            user = TelegramUser.objects.get(telegram_id=int(telegram_id))
            return user.language or 'uz_latin'
        except (TelegramUser.DoesNotExist, ValueError, TypeError):
            pass
    return request.GET.get('lang') or 'uz_latin'


def _serialize_live_stream(stream, language, request, with_winners=False):
    banner_url = None
    if stream.banner:
        try:
            banner_url = request.build_absolute_uri(stream.banner.url)
        except (ValueError, AttributeError):
            banner_url = None
    data = {
        'id': stream.id,
        'title': stream.get_title(language),
        'description': stream.get_description(language),
        'scheduled_at': stream.scheduled_at.isoformat(),
        'stream_url': stream.stream_url,
        'banner': banner_url,
        'participants_count': stream.participants_count,
        'is_past': stream.is_past,
    }
    if with_winners:
        winners_qs = stream.winners.select_related('user').all()
        electricians = []
        sellers = []
        for w in winners_qs:
            entry = {
                'position': w.position,
                'name': (w.user.first_name or '').strip() or w.user.username or f'ID {w.user.telegram_id}',
                'telegram_id': w.user.telegram_id,
                'prize_text': w.get_prize_text(language),
            }
            if w.user.user_type == 'santenik':
                electricians.append(entry)
            elif w.user.user_type == 'sotuvchi':
                sellers.append(entry)
        data['winners'] = {
            'electricians': electricians,
            'sellers': sellers,
        }
    return data


@api_view(['GET'])
@permission_classes([AllowAny])
@no_cache_response
def get_live_streams(request):
    """Список активных прямых эфиров (предстоящих и прошедших)."""
    language = _live_stream_language(request)
    streams = LiveStream.objects.filter(is_active=True).order_by('-scheduled_at')
    now = timezone.now()
    upcoming = []
    past = []
    for s in streams:
        item = _serialize_live_stream(s, language, request)
        (past if s.scheduled_at < now else upcoming).append(item)
    upcoming.sort(key=lambda x: x['scheduled_at'])
    return Response({'upcoming': upcoming, 'past': past})


@api_view(['GET'])
@permission_classes([AllowAny])
@no_cache_response
def get_live_stream_detail(request, stream_id):
    """Детальная информация по эфиру с группировкой победителей."""
    language = _live_stream_language(request)
    try:
        stream = LiveStream.objects.get(id=stream_id, is_active=True)
    except LiveStream.DoesNotExist:
        return Response({'error': 'Live stream not found'}, status=status.HTTP_404_NOT_FOUND)
    return Response(_serialize_live_stream(stream, language, request, with_winners=True))


@api_view(['GET'])
@permission_classes([AllowAny])
@no_cache_response
def get_top_users(request):
    """Лидерборд по реальным баллам (earned - spent).

    Query params:
        telegram_id — текущий пользователь (для определения user_type).
        user_type   — 'electrician' | 'seller'. По умолчанию берётся тип текущего пользователя.
        period      — 'all' (по умолчанию) или 'current' (текущий месяц).
        limit       — сколько строк вернуть (по умолчанию 20, максимум 100).
    """
    telegram_id = request.GET.get('telegram_id')
    period = (request.GET.get('period') or 'all').strip().lower()
    user_type = (request.GET.get('user_type') or '').strip().lower()
    try:
        limit = max(1, min(int(request.GET.get('limit', 20)), 100))
    except (TypeError, ValueError):
        limit = 20

    current_user = None
    if telegram_id:
        try:
            current_user = TelegramUser.objects.filter(telegram_id=int(telegram_id)).first()
        except (TypeError, ValueError):
            current_user = None

    if user_type not in ('santenik', 'seller'):
        user_type = current_user.user_type if current_user and current_user.user_type else 'electrician'

    def _display_name(u):
        parts = [u.first_name or '', u.last_name or '']
        name = ' '.join(p for p in parts if p).strip()
        if not name:
            name = u.username or f'ID {u.telegram_id}'
        return name

    if period == 'all':
        # Real balance already stored in TelegramUser.points
        leaderboard_qs = (
            TelegramUser.objects
            .filter(user_type=user_type, is_active=True, points__gt=0)
            .annotate(
                scans=models.Count(
                    'scanned_qrcodes',
                    filter=models.Q(scanned_qrcodes__is_scanned=True, scanned_qrcodes__is_deleted=False),
                )
            )
            .order_by('-points')[:limit]
        )
        items = []
        current_user_in_top = False
        for idx, u in enumerate(leaderboard_qs, start=1):
            is_me = bool(current_user and current_user.id == u.id)
            if is_me:
                current_user_in_top = True
            items.append({
                'position': idx,
                'telegram_id': u.telegram_id,
                'name': _display_name(u),
                'points': u.points,
                'scans': u.scans,
                'is_me': is_me,
            })

        me = None
        if current_user and current_user.user_type == user_type:
            current_user.calculate_points()
            my_points = current_user.points
            my_scans = QRCode.objects.filter(
                scanned_by=current_user, is_scanned=True, is_deleted=False,
            ).count()
            my_position = (
                TelegramUser.objects
                .filter(user_type=user_type, is_active=True, points__gt=my_points)
                .count()
            ) + 1 if my_points > 0 else None
            me = {
                'telegram_id': current_user.telegram_id,
                'name': _display_name(current_user),
                'points': my_points,
                'scans': my_scans,
                'position': my_position,
                'in_top': current_user_in_top,
            }
    else:
        # Monthly: earned this month minus gifts redeemed this month
        now = timezone.localtime(timezone.now())
        month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        from datetime import timedelta
        next_month = (month_start + timedelta(days=32)).replace(day=1)

        earned_rows = list(
            QRCode.objects
            .filter(
                is_scanned=True,
                is_deleted=False,
                scanned_by__isnull=False,
                scanned_by__user_type=user_type,
                scanned_by__is_active=True,
                scanned_at__gte=month_start,
                scanned_at__lt=next_month,
            )
            .values('scanned_by_id')
            .annotate(earned=models.Sum('points'), scans=models.Count('id'))
        )
        if not earned_rows:
            return Response({'user_type': user_type, 'period': 'current', 'items': [], 'me': None})

        user_ids = [r['scanned_by_id'] for r in earned_rows]
        earned_map = {r['scanned_by_id']: r['earned'] for r in earned_rows}
        scans_map = {r['scanned_by_id']: r['scans'] for r in earned_rows}

        spent_rows = list(
            GiftRedemption.objects
            .filter(
                user_id__in=user_ids,
                requested_at__gte=month_start,
                requested_at__lt=next_month,
            )
            .exclude(status__in=['rejected', 'cancelled_by_user', 'not_received'])
            .values('user_id')
            .annotate(spent=models.Sum('gift__points_cost'))
        )
        spent_map = {r['user_id']: r['spent'] for r in spent_rows}

        net_list = sorted(
            [(uid, max(0, earned_map[uid] - spent_map.get(uid, 0))) for uid in user_ids],
            key=lambda x: -x[1],
        )[:limit]
        top_ids = [uid for uid, _ in net_list]
        net_map = {uid: net for uid, net in net_list}

        users_by_id = {
            u.id: u
            for u in TelegramUser.objects.filter(id__in=top_ids).only(
                'id', 'telegram_id', 'first_name', 'last_name', 'username',
            )
        }
        items = []
        current_user_in_top = False
        for idx, uid in enumerate(top_ids, start=1):
            u = users_by_id.get(uid)
            if not u:
                continue
            is_me = bool(current_user and current_user.id == u.id)
            if is_me:
                current_user_in_top = True
            items.append({
                'position': idx,
                'telegram_id': u.telegram_id,
                'name': _display_name(u),
                'points': net_map[uid],
                'scans': scans_map.get(uid, 0),
                'is_me': is_me,
            })

        me = None
        if current_user and current_user.user_type == user_type:
            my_earned = earned_map.get(current_user.id, 0)
            my_spent = spent_map.get(current_user.id, 0)
            my_points = max(0, my_earned - my_spent)
            my_scans = scans_map.get(current_user.id, 0)
            my_position = sum(1 for _, net in net_list if net > my_points) + 1 if my_points > 0 else None
            me = {
                'telegram_id': current_user.telegram_id,
                'name': _display_name(current_user),
                'points': my_points,
                'scans': my_scans,
                'position': my_position,
                'in_top': current_user_in_top,
            }

    return Response({
        'user_type': user_type,
        'period': period if period in ('all', 'current') else 'all',
        'items': items,
        'me': me,
    })


# ──────────────────────────────────────────────────────────────────────────────
# Seller Web App views (HMAC initData auth)
# ──────────────────────────────────────────────────────────────────────────────

def _get_seller_user(request):
    """Validate X-Telegram-Init-Data and return the sotuvchi TelegramUser.

    Returns (user, None) on success or (None, Response) on failure.
    """
    import hashlib
    import hmac as _hmac
    import json
    import urllib.parse

    init_data = request.headers.get('X-Telegram-Init-Data', '')
    if not init_data:
        return None, Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

    token = settings.TELEGRAM_BOT_TOKEN
    if not token:
        return None, Response({'error': 'Server misconfigured'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    params = dict(urllib.parse.parse_qsl(init_data, keep_blank_values=True))
    hash_val = params.pop('hash', None)
    if not hash_val:
        return None, Response({'error': 'Invalid init data'}, status=status.HTTP_401_UNAUTHORIZED)

    data_check = '\n'.join(f"{k}={v}" for k, v in sorted(params.items()))
    secret_key = _hmac.new(b'WebAppData', token.encode(), hashlib.sha256).digest()
    expected_hash = _hmac.new(secret_key, data_check.encode(), hashlib.sha256).hexdigest()

    if not _hmac.compare_digest(expected_hash, hash_val):
        return None, Response({'error': 'Invalid signature'}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        tg_user_data = json.loads(params.get('user', '{}'))
        tg_id = int(tg_user_data.get('id', 0))
    except (ValueError, TypeError):
        return None, Response({'error': 'Invalid user data'}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        user = TelegramUser.objects.get(telegram_id=tg_id)
    except TelegramUser.DoesNotExist:
        return None, Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    if user.user_type != 'sotuvchi':
        return None, Response({'error': 'Access denied'}, status=status.HTTP_403_FORBIDDEN)

    return user, None


def seller_webapp_view(request):
    """Sotuvchi uchun Telegram Mini App sahifasi."""
    import time
    context = {
        'user_language': 'uz_latin',
        'app_version': str(int(time.time())),
    }
    response = render(request, 'webapp/seller.html', context)
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0, private'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response


@api_view(['GET'])
@permission_classes([AllowAny])
@no_cache_response
def seller_dashboard(request):
    """Sotuvchi dashboard: balans, batch statistika.

    Yangi model: ball to'g'ridan-to'g'ri sotuvchiga biriktiriladi (store yo'q).
    """
    from django.db.models import Sum, Count, Q

    user, err = _get_seller_user(request)
    if err:
        return err

    # Sotuvchining barcha ball tranzaksiyalari
    points_total = SellerPointsTransaction.objects.filter(
        seller=user,
    ).aggregate(total=Sum('points'))['total'] or 0

    # Sotuvchining barcha batchlari (seller FK orqali)
    batches = QRCodeBatch.objects.filter(seller=user)
    qr_total = sum(b.quantity for b in batches)
    qr_scanned = batches.aggregate(
        scanned=Count('qr_codes', filter=Q(qr_codes__is_scanned=True, qr_codes__is_deleted=False))
    )['scanned'] or 0

    # Region — TelegramUser dan
    region_name = None
    if user.region_id:
        region_name = user.region.name_uz or user.region.name_ru or user.region.code

    full_name = ' '.join(filter(None, [user.first_name, user.last_name])) or 'Sotuvchi'

    return Response({
        'seller_name': full_name,
        'seller_first_name': user.first_name or 'Sotuvchi',
        'seller_phone': user.phone_number or '',
        'seller_username': user.username or '',
        'region': region_name,
        'points': int(points_total),
        'qr_total': qr_total,
        'qr_scanned': qr_scanned,
    })


@api_view(['GET'])
@permission_classes([AllowAny])
@no_cache_response
def seller_transactions(request):
    """Sotuvchi ball tranzaksiyalari ro'yxati (oxirgi 50 ta).

    Yangi model: store filter olib tashlandi, faqat seller bo'yicha.
    """
    user, err = _get_seller_user(request)
    if err:
        return err

    txs = SellerPointsTransaction.objects.filter(
        seller=user,
    ).order_by('-created_at')[:50]

    results = [
        {
            'id': tx.id,
            'transaction_type': tx.transaction_type,
            'transaction_type_display': tx.get_transaction_type_display(),
            'points': tx.points,
            'note': tx.note or '',
            'created_at': tx.created_at.strftime('%d.%m.%Y %H:%M'),
        }
        for tx in txs
    ]
    return Response({'results': results})


@api_view(['GET'])
@permission_classes([AllowAny])
@no_cache_response
def seller_batches(request):
    """Sotuvchining batch'lar ro'yxati (oxirgi 20 ta).

    Yangi model: store filter olib tashlandi, faqat seller bo'yicha.
    """
    user, err = _get_seller_user(request)
    if err:
        return err

    batches = QRCodeBatch.objects.filter(seller=user).order_by('-created_at')[:20]

    results = [
        {
            'id': b.id,
            'name': b.name,
            'quantity': b.quantity,
            'scanned': b.qr_codes.filter(is_scanned=True, is_deleted=False).count(),
            'status': b.status,
            'status_display': b.get_status_display(),
            'delivery_status': b.delivery_status,
            'delivery_status_display': b.get_delivery_status_display(),
            'created_at': b.created_at.strftime('%d.%m.%Y'),
        }
        for b in batches
    ]
    return Response({'results': results})


@api_view(['GET'])
@permission_classes([AllowAny])
@no_cache_response
def seller_balance_history(request):
    """Sotuvchi balans tarixi — oxirgi 30 kun."""
    from django.db.models import Sum
    from datetime import timedelta

    user, err = _get_seller_user(request)
    if err:
        return err

    today = timezone.localdate()
    start_date = today - timedelta(days=29)

    # Har kun uchun ball summasi
    txs = SellerPointsTransaction.objects.filter(
        seller=user,
        created_at__date__gte=start_date,
    ).values_list('created_at', 'points')

    # Kumulyativ balans tayyorlash
    daily = {(start_date + timedelta(days=i)): 0 for i in range(30)}
    for created_at, points in txs:
        d = timezone.localtime(created_at).date()
        if d in daily:
            daily[d] += points

    # 30 kungacha bo'lgan boshlang'ich balans
    base = SellerPointsTransaction.objects.filter(
        seller=user,
        created_at__date__lt=start_date,
    ).aggregate(s=Sum('points'))['s'] or 0

    labels, values = [], []
    running = int(base)
    for d in sorted(daily.keys()):
        running += int(daily[d])
        labels.append(d.strftime('%d.%m'))
        values.append(running)

    return Response({
        'labels': labels,
        'values': values,
        'current': running,
        'period_change': int(sum(daily.values())),
    })


@api_view(['GET'])
@permission_classes([AllowAny])
@no_cache_response
def seller_batch_qr_detail(request, batch_id):
    """Bitta batchning QR kodlari (oxirgi 200 ta) — skanlangan/skanlanmagan."""
    user, err = _get_seller_user(request)
    if err:
        return err

    try:
        batch = QRCodeBatch.objects.get(pk=batch_id, seller=user)
    except QRCodeBatch.DoesNotExist:
        return Response({'error': 'Batch topilmadi'}, status=status.HTTP_404_NOT_FOUND)

    qrs = batch.qr_codes.filter(is_deleted=False).select_related('scanned_by').order_by('-is_scanned', '-scanned_at')[:200]
    results = [
        {
            'serial': q.serial_number,
            'code': q.code,
            'is_scanned': q.is_scanned,
            'points': q.points,
            'scanned_at': timezone.localtime(q.scanned_at).strftime('%d.%m.%Y %H:%M') if q.scanned_at else None,
            'scanned_by': (q.scanned_by.first_name or q.scanned_by.username or 'Foydalanuvchi') if q.scanned_by_id else None,
        }
        for q in qrs
    ]
    return Response({
        'batch_name': batch.name,
        'quantity': batch.quantity,
        'scanned_count': sum(1 for r in results if r['is_scanned']),
        'results': results,
    })


@api_view(['GET'])
@permission_classes([AllowAny])
@no_cache_response
def seller_top_santexniks(request):
    """Sotuvchining batchlaridan QR skanlagan top santexniklar.

    Store o'rniga endi seller.batches dagi QRlarni ko'ramiz.
    """
    from django.db.models import Count, Sum

    user, err = _get_seller_user(request)
    if err:
        return err

    seller_batch_ids = list(QRCodeBatch.objects.filter(seller=user).values_list('id', flat=True))
    if not seller_batch_ids:
        return Response({'results': []})

    top = (
        TelegramUser.objects.filter(
            scanned_qrcodes__batch_id__in=seller_batch_ids,
            scanned_qrcodes__is_scanned=True,
            scanned_qrcodes__is_deleted=False,
            user_type='santenik',
        )
        .annotate(
            scans=Count('scanned_qrcodes', distinct=True),
            earned=Sum('scanned_qrcodes__points'),
        )
        .order_by('-scans')[:20]
    )

    results = [
        {
            'rank': i + 1,
            'name': (u.first_name or u.username or f'ID {u.telegram_id}'),
            'phone': u.phone_number or '',
            'scans': u.scans,
            'earned': int(u.earned or 0),
        }
        for i, u in enumerate(top)
    ]
    return Response({'results': results, 'total_count': len(results)})


@api_view(['GET'])
@permission_classes([AllowAny])
@no_cache_response
def seller_commission_calc(request):
    """Komissiya kalkulyatori — sotuv summasi → komissiya hisobi.

    Query: ?sales=10000 (USD)
    Store yo'q — default komissiya 5% (yoki kelajakda sotuvchi modeliga qo'shiladi).
    """
    user, err = _get_seller_user(request)
    if err:
        return err

    try:
        sales = float(request.GET.get('sales', 0) or 0)
    except ValueError:
        sales = 0

    # Default komissiya — eski store dan olib bo'lsa olamiz, aks holda 5%
    commission_percent = 5.0
    store = user.owned_stores.first()
    if store and store.commission_percent:
        commission_percent = float(store.commission_percent)
    commission_amount = round(sales * commission_percent / 100, 2)

    return Response({
        'sales': sales,
        'commission_percent': commission_percent,
        'commission_amount': commission_amount,
        'store_name': user.first_name or 'Sotuvchi',
    })
