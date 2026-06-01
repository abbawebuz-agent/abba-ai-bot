"""
Celery tasks for core app.
"""
import csv
import io
import os
import zipfile
import asyncio
import logging
from celery import shared_task, chain
from django.conf import settings
from django.utils import timezone
from aiogram import Bot
from .models import QRCode, QRCodeBatch, BroadcastMessage, TelegramUser
from .utils import generate_qr_code_image, generate_qr_codes_batch, generate_qr_code_images_batch
from .messaging import send_message_to_user, TELEGRAM_MESSAGE_DELAY

logger = logging.getLogger(__name__)


@shared_task
def generate_promo_codes_task(quantity: int, points: int = 50):
    """N ta promokod yaratadi — batch'siz, S+7 alphanumeric format.

    Har biri global `sequence_number` oladi. Keyinchalik admin sotuvchi
    panelida `SellerBatch(promo_from..promo_to)` orqali sotuvchiga
    biriktirilishi mumkin.
    """
    try:
        qty = int(quantity)
        pts = int(points)
    except (TypeError, ValueError):
        logger.error(f"generate_promo_codes_task: noto'g'ri parametr {quantity=} {points=}")
        return

    if qty <= 0:
        return

    created = 0
    for _ in range(qty):
        try:
            QRCode.create_promo_code(points=pts)
            created += 1
        except Exception as exc:
            logger.exception(f"create_promo_code xato (created so far: {created}): {exc}")
            # Davom ettiramiz — bitta xato butun batch'ni to'xtatmasin

    logger.info(f"generate_promo_codes_task: {created}/{qty} ta promokod yaratildi ({pts} ball)")
    return {'requested': qty, 'created': created, 'points': pts}


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def generate_batch_zip(self, batch_id: int):
    """
    QRCodeBatch uchun QR kartalar yaratib ZIP arxiv tayyorlaydi.

    1. Batch'ni 'processing' ga o'tkazadi
    2. quantity ta QRCode.create_code(batch) chaqiradi
    3. Har QR uchun PNG rasm generatsiya qiladi (qrcode + Pillow)
    4. Barcha rasmlarni + CSV ro'yxatni ZIP ga soladi
    5. Batch'ni 'completed' ga o'tkazadi va zip_file saqlanadi

    Rasm formati: JIP_{serial}.png (600×600 px, aqlli dizayn)
    ZIP ichi: images/ papka + codes.csv
    """
    try:
        batch = QRCodeBatch.objects.select_related('store').get(id=batch_id)
    except QRCodeBatch.DoesNotExist:
        logger.error(f"generate_batch_zip: batch {batch_id} topilmadi")
        return

    if batch.status == 'active':
        logger.warning(f"generate_batch_zip: batch {batch_id} allaqachon active — o'tkazildi")
        return
    # 'inactive' yoki qiymat yo'q — davom etamiz
    logger.info(f"generate_batch_zip: batch {batch_id} ({batch.name}) boshlandi, {batch.quantity} ta")

    try:
        _do_generate_batch_zip(batch)
    except Exception as exc:
        logger.error(f"generate_batch_zip: batch {batch_id} xatolik: {exc}", exc_info=True)
        batch.status = 'failed'
        batch.error_message = str(exc)[:2000]
        batch.save(update_fields=['status', 'error_message'])
        raise self.retry(exc=exc)


def _do_generate_batch_zip(batch: QRCodeBatch):
    """Asosiy generatsiya logikasi (sinxron, Celery worker'da ishlaydi)."""
    import qrcode as qrcode_lib
    from PIL import Image, ImageDraw, ImageFont

    # 1. QR kartalarni DB ga yozamiz
    qr_list = []
    for _ in range(batch.quantity):
        qr = QRCode.create_code(batch)
        qr_list.append(qr)

    logger.info(f"  {len(qr_list)} ta QRCode yaratildi, rasm generatsiya boshlanadi...")

    # 2. ZIP arxiv tayyorlash
    zip_dir = os.path.join(settings.MEDIA_ROOT, 'batches')
    os.makedirs(zip_dir, exist_ok=True)
    timestamp = timezone.now().strftime('%Y%m%d_%H%M%S')
    zip_filename = f"batch_{batch.id}_{timestamp}.zip"
    zip_path = os.path.join(zip_dir, zip_filename)

    bot_username = getattr(settings, 'TELEGRAM_BOT_USERNAME', '')
    instruction = f"@{bot_username} ga kiring va kodni kiriting" if bot_username else "Botga o'ting va kodni kiriting"

    with zipfile.ZipFile(zip_path, 'w', compression=zipfile.ZIP_DEFLATED) as zf:
        # CSV ro'yxat
        csv_buf = io.StringIO()
        writer = csv.writer(csv_buf)
        writer.writerow(['serial_number', 'sequence_number', 'code', 'hash_code', 'points', 'store'])
        for qr in qr_list:
            store_name = batch.store.name if batch.store else '—'
            writer.writerow([qr.serial_number, qr.sequence_number, qr.code, qr.hash_code, qr.points, store_name])
        zf.writestr('codes.csv', csv_buf.getvalue())

        # PNG rasmlar
        for qr in qr_list:
            try:
                img_bytes = _render_scratch_card(qr, batch, instruction)
                zf.writestr(f"images/{qr.serial_number}.png", img_bytes)
            except Exception as e:
                logger.warning(f"  Rasm xatolik ({qr.serial_number}): {e}")

    # 3. Batch'ni yangilaymiz — yangi status modeli: 'active' (faollashtirilgan)
    batch.zip_file.name = f"batches/{zip_filename}"
    batch.status = 'active'
    batch.completed_at = timezone.now()
    batch.save(update_fields=['zip_file', 'status', 'completed_at', 'error_message'])
    logger.info(f"  Batch {batch.id} tayyor: {zip_path}")


def _render_scratch_card(qr, batch, instruction: str) -> bytes:
    """
    Bitta skretch-karta PNG rasmi (600×600 px).

    Tuzilma:
    - Yuqori chiziq: JIP brendi
    - Markazda: katta kod matni
    - Pastda: seriya raqami va ko'rsatma
    Pillow bilan chiziladi — Playwright talab qilinmaydi.
    """
    import qrcode as qrcode_lib
    from PIL import Image, ImageDraw, ImageFont

    W, H = 600, 600
    BG = (255, 255, 255)
    BLUE = (25, 118, 210)
    DARK = (30, 30, 30)
    GRAY = (120, 120, 120)

    img = Image.new('RGB', (W, H), BG)
    draw = ImageDraw.Draw(img)

    # Header
    draw.rectangle([(0, 0), (W, 70)], fill=BLUE)
    try:
        font_h = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 28)
        font_code = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 52)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
        font_serial = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
    except Exception:
        font_h = font_code = font_small = font_serial = ImageFont.load_default()

    # JIP nomi
    draw.text((W // 2, 35), "JIP", fill=(255, 255, 255), font=font_h, anchor="mm")

    # QR mini rasm (optional, agar qrcode lib ishlasa)
    try:
        qr_img = qrcode_lib.make(qr.code)
        qr_img = qr_img.resize((150, 150))
        img.paste(qr_img, ((W - 150) // 2, 90))
    except Exception:
        pass

    # Kod matni (katta, markazda)
    draw.text((W // 2, 310), qr.code, fill=DARK, font=font_code, anchor="mm")

    # Separator chiziq
    draw.rectangle([(40, 380), (W - 40, 382)], fill=GRAY)

    # Ball miqdori
    draw.text((W // 2, 410), f"+{qr.points} ball", fill=BLUE, font=font_small, anchor="mm")

    # Do'kon nomi
    draw.text((W // 2, 450), batch.store.name[:40], fill=GRAY, font=font_serial, anchor="mm")

    # Ko'rsatma
    draw.text((W // 2, 490), instruction[:60], fill=GRAY, font=font_serial, anchor="mm")

    # Seriya raqami
    draw.text((W // 2, 560), f"SN: {qr.serial_number}", fill=GRAY, font=font_serial, anchor="mm")

    # Chegara
    draw.rectangle([(2, 2), (W - 3, H - 3)], outline=BLUE, width=3)

    buf = io.BytesIO()
    img.save(buf, format='PNG', optimize=True)
    return buf.getvalue()



@shared_task(bind=True)
def send_broadcast_batch(self, broadcast_id, user_ids, batch_number, total_batches):
    """
    Отправляет батч сообщений пользователям.
    
    Args:
        broadcast_id: ID объекта BroadcastMessage
        user_ids: Список ID пользователей для отправки
        batch_number: Номер текущего батча
        total_batches: Общее количество батчей
    """
    try:
        broadcast = BroadcastMessage.objects.get(id=broadcast_id)

        # Получаем пользователей
        users = list(TelegramUser.objects.filter(id__in=user_ids))

        photo_path = None
        if broadcast.image:
            try:
                photo_path = broadcast.image.path
            except (ValueError, OSError):
                pass

        async def send_batch():
            bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
            try:
                sent = 0
                failed = 0

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
                            sent += 1
                        else:
                            failed += 1
                            logger.warning(f"Не удалось отправить пользователю {user.telegram_id}: {error}")

                        # Соблюдаем лимит Telegram API
                        if i < len(users) - 1:
                            await asyncio.sleep(TELEGRAM_MESSAGE_DELAY)

                    except Exception as e:
                        logger.error(f"Ошибка при отправке пользователю {user.telegram_id}: {e}")
                        failed += 1

                return sent, failed
            finally:
                await bot.session.close()

        sent, failed = asyncio.run(send_batch())

        # Обновляем статистику рассылки
        broadcast.sent_count += sent
        broadcast.failed_count += failed
        broadcast.save(update_fields=['sent_count', 'failed_count'])

        logger.info(
            f"Батч {batch_number}/{total_batches} рассылки '{broadcast.title}' завершен: "
            f"отправлено {sent}, ошибок {failed}"
        )

        return {
            'batch_number': batch_number,
            'sent': sent,
            'failed': failed
        }

    except BroadcastMessage.DoesNotExist:
        logger.error(f"Рассылка {broadcast_id} не найдена")
        return {'error': f'Broadcast {broadcast_id} not found'}
    except Exception as e:
        logger.error(f"Ошибка при отправке батча {batch_number}: {e}")
        # Обновляем статистику ошибок
        try:
            broadcast = BroadcastMessage.objects.get(id=broadcast_id)
            broadcast.failed_count += len(user_ids)
            broadcast.save(update_fields=['failed_count'])
        except:
            pass
        raise


# Порог: при большем числе получателей рассылка по области идёт в фоне (Celery)
REGION_MESSAGE_ASYNC_THRESHOLD = getattr(
    settings, 'REGION_MESSAGE_ASYNC_THRESHOLD', 100
)


@shared_task(bind=True, soft_time_limit=3600)
def send_region_message_task(
        self,
        log_id,
        region_code,
        message_text,
        image_storage_path,
        user_type_filter,
        language_filter,
):
    """
    Отправляет сообщение по области в фоне (лимиты Telegram, без таймаута админки).
    Вызывается из админки при числе получателей > REGION_MESSAGE_ASYNC_THRESHOLD.
    Обновляет RegionMessageLog по завершении.
    """
    from core.regions import get_user_region_code
    from core.models import RegionMessageLog
    from django.core.files.storage import default_storage
    from django.utils import timezone

    def update_log(sent, failed, status='completed', error_msg=''):
        try:
            log = RegionMessageLog.objects.get(id=log_id)
            log.sent_count = sent
            log.failed_count = failed
            log.status = status
            log.completed_at = timezone.now()
            if error_msg:
                log.error_message = error_msg
            log.save()
        except RegionMessageLog.DoesNotExist:
            pass

    # Отложенная рассылка: уважаем отмену, иначе помечаем как running.
    try:
        log = RegionMessageLog.objects.get(id=log_id)
        if log.status == 'cancelled':
            logger.info('send_region_message_task: лог %s отменён, выходим', log_id)
            return {'sent': 0, 'failed': 0, 'total': 0, 'cancelled': True}
        if log.status == 'pending':
            log.status = 'running'
            log.save(update_fields=['status'])
    except RegionMessageLog.DoesNotExist:
        pass

    users_qs = TelegramUser.objects.filter(
        latitude__isnull=False,
        longitude__isnull=False,
        is_active=True,
    )
    if user_type_filter:
        users_qs = users_qs.filter(user_type=user_type_filter)
    if language_filter:
        users_qs = users_qs.filter(language=language_filter)

    users = list(users_qs)
    if region_code == 'all':
        filtered = users
    else:
        filtered = [
            u for u in users
            if get_user_region_code(u) == region_code
        ]
    if not filtered:
        msg = 'Нет пользователей с координатами' if region_code == 'all' else f'В области {region_code} нет пользователей'
        logger.warning('send_region_message_task: %s', msg)
        update_log(0, 0, status='completed', error_msg=msg)
        return {'sent': 0, 'failed': 0, 'total': 0}

    if not message_text and not image_storage_path:
        msg = 'Рассылка отменена: не указан текст и изображение'
        logger.error('send_region_message_task: %s', msg)
        update_log(0, 0, status='failed', error_msg=msg)
        return {'sent': 0, 'failed': 0, 'total': 0}

    photo_path = None
    if image_storage_path and default_storage.exists(image_storage_path):
        import tempfile
        with default_storage.open(image_storage_path, 'rb') as f:
            ext = os.path.splitext(image_storage_path)[1] or '.jpg'
            with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
                tmp.write(f.read())
                photo_path = tmp.name
    try:
        async def _send_all():
            bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
            sent, failed = 0, 0
            try:
                for i, user in enumerate(filtered):
                    success, err = await send_message_to_user(
                        bot=bot,
                        user=user,
                        text=message_text or '',
                        parse_mode='HTML',
                        photo_path=photo_path,
                        disable_link_preview=True,
                    )
                    if success:
                        sent += 1
                    else:
                        failed += 1
                    if i < len(filtered) - 1:
                        await asyncio.sleep(TELEGRAM_MESSAGE_DELAY)
                return sent, failed
            finally:
                await bot.session.close()

        sent, failed = asyncio.run(_send_all())
        logger.info(
            'Рассылка по области %s завершена: отправлено %s, ошибок %s (всего %s)',
            region_code, sent, failed, len(filtered),
        )
        update_log(sent, failed, status='completed')
        return {'sent': sent, 'failed': failed, 'total': len(filtered)}
    except Exception as e:
        logger.exception('send_region_message_task: ошибка при рассылке')
        update_log(0, len(filtered), status='failed', error_msg=str(e))
        raise
    finally:
        if photo_path and os.path.exists(photo_path):
            try:
                os.unlink(photo_path)
            except OSError:
                pass
        if image_storage_path and default_storage.exists(image_storage_path):
            try:
                default_storage.delete(image_storage_path)
            except Exception:
                pass


@shared_task(bind=True)
def send_broadcast_chained(self, broadcast_id):
    """
    Запускает цепочку задач для отправки большой рассылки.
    Разбивает пользователей на батчи и отправляет последовательно.
    
    Args:
        broadcast_id: ID объекта BroadcastMessage
    """
    try:
        broadcast = BroadcastMessage.objects.get(id=broadcast_id)

        if not broadcast.message_text and not broadcast.image:
            broadcast.status = 'failed'
            broadcast.save(update_fields=['status'])
            logger.error('send_broadcast_chained: рассылка %s отменена — нет текста и изображения', broadcast_id)
            return {'error': 'empty message'}

        # Получаем список пользователей с применением фильтров
        users_query = TelegramUser.objects.filter(is_active=True)

        # Фильтр по типу пользователя
        if broadcast.user_type_filter:
            users_query = users_query.filter(user_type=broadcast.user_type_filter)

        # Фильтр по языку
        if broadcast.language_filter:
            users_query = users_query.filter(language=broadcast.language_filter)

        # Фильтр по региону
        if broadcast.region_filter:
            from core.regions import get_user_region_code

            users_with_location = list(users_query.filter(
                latitude__isnull=False,
                longitude__isnull=False
            ))

            filtered_user_ids = []
            for user in users_with_location:
                user_region = get_user_region_code(user)
                if user_region == broadcast.region_filter:
                    filtered_user_ids.append(user.id)

            if filtered_user_ids:
                users_query = users_query.filter(id__in=filtered_user_ids)
            else:
                users_query = users_query.none()

        user_ids = list(users_query.values_list('id', flat=True))
        total_users = len(user_ids)

        # Обновляем статистику рассылки
        broadcast.total_users = total_users
        broadcast.status = 'sending'
        broadcast.started_at = timezone.now()
        broadcast.save(update_fields=['total_users', 'status', 'started_at'])

        # Размер батча (можно настроить через settings)
        BATCH_SIZE = getattr(settings, 'BROADCAST_BATCH_SIZE', 1000)

        # Разбиваем на батчи
        batches = []
        for i in range(0, total_users, BATCH_SIZE):
            batch_user_ids = user_ids[i:i + BATCH_SIZE]
            batches.append(batch_user_ids)

        total_batches = len(batches)

        logger.info(
            f"Начало рассылки '{broadcast.title}' для {total_users} пользователей "
            f"({total_batches} батчей по {BATCH_SIZE} пользователей)"
        )

        # Создаем цепочку задач
        if batches:
            # Создаем задачи для каждого батча
            tasks = []
            for batch_num, batch_user_ids in enumerate(batches, 1):
                task = send_broadcast_batch.s(
                    broadcast_id=broadcast_id,
                    user_ids=batch_user_ids,
                    batch_number=batch_num,
                    total_batches=total_batches
                )
                tasks.append(task)

            # Добавляем задачу завершения в конец цепочки
            tasks.append(finalize_broadcast.s(broadcast_id=broadcast_id))

            # Запускаем цепочку задач последовательно
            chain(*tasks).apply_async()

            logger.info(f"Запущена цепочка из {total_batches + 1} задач для рассылки {broadcast_id}")
        else:
            # Если нет пользователей, завершаем рассылку
            broadcast.status = 'completed'
            broadcast.completed_at = timezone.now()
            broadcast.save(update_fields=['status', 'completed_at'])
            logger.info(f"Рассылка '{broadcast.title}' не имеет пользователей для отправки")

        return {
            'total_users': total_users,
            'total_batches': total_batches,
            'batch_size': BATCH_SIZE
        }

    except BroadcastMessage.DoesNotExist:
        logger.error(f"Рассылка {broadcast_id} не найдена")
        return {'error': f'Broadcast {broadcast_id} not found'}
    except Exception as e:
        logger.error(f"Ошибка при запуске рассылки {broadcast_id}: {e}")
        try:
            broadcast = BroadcastMessage.objects.get(id=broadcast_id)
            broadcast.status = 'failed'
            broadcast.save(update_fields=['status'])
        except:
            pass
        raise


@shared_task(bind=True)
def finalize_broadcast(self, broadcast_id):
    """
    Завершает рассылку после отправки всех батчей.
    
    Args:
        broadcast_id: ID объекта BroadcastMessage
    """
    try:
        broadcast = BroadcastMessage.objects.get(id=broadcast_id)
        broadcast.status = 'completed'
        broadcast.completed_at = timezone.now()
        broadcast.save(update_fields=['status', 'completed_at'])

        logger.info(
            f"Рассылка '{broadcast.title}' завершена: "
            f"отправлено {broadcast.sent_count}, ошибок {broadcast.failed_count} из {broadcast.total_users}"
        )

        return {
            'total': broadcast.total_users,
            'sent': broadcast.sent_count,
            'failed': broadcast.failed_count
        }
    except BroadcastMessage.DoesNotExist:
        logger.error(f"Рассылка {broadcast_id} не найдена")
        return {'error': f'Broadcast {broadcast_id} not found'}


@shared_task(bind=True)
def dispatch_monthly_role_reminder(self):
    """
    Beat-таск: 1-го числа каждого месяца отправляет push-уведомление
    пользователям, которые не выбрали роль или не завершили регистрацию.

    Расписание: Beat дёргает таск каждые 15 мин в течение 1-го числа.
    Таск сам решает, нужно ли что-то делать (по time_of_day из настроек
    и по флагу month_key — чтобы не отправить дважды).

    Критерий «регистрация не завершена» — повторяет bot.bot.is_registration_complete.
    """
    from .models import (
        MonthlyReminderSettings, MonthlyReminderLog, TelegramUser,
    )
    from django.db import IntegrityError
    from django.db.models import Q
    import tempfile

    settings_obj = MonthlyReminderSettings.objects.first()
    if not settings_obj or not settings_obj.is_active:
        return {'skipped': 'disabled'}

    now = timezone.now()
    local_now = timezone.localtime(now)
    today = local_now.date()
    if today.day != 1:
        return {'skipped': 'not first day of month'}
    if local_now.time() < settings_obj.time_of_day:
        return {'skipped': 'before time_of_day', 'time_of_day': str(settings_obj.time_of_day)}

    month_key = today.strftime('%Y-%m')
    # Атомарный захват месяца: уникальный индекс не даст создать дубль.
    try:
        log = MonthlyReminderLog.objects.create(
            month_key=month_key,
            status='running',
            total=0,
        )
    except IntegrityError:
        # Уже запущено в этом месяце — выходим.
        return {'skipped': 'already processed', 'month_key': month_key}

    # Регистрация не завершена: одно из обязательных полей пусто.
    # (Совпадает с bot.bot.is_registration_complete.)
    incomplete = (
        Q(language__isnull=True) | Q(language='') |
        Q(first_name__isnull=True) | Q(first_name='') |
        Q(user_type__isnull=True) | Q(user_type='') |
        Q(privacy_accepted=False) |
        Q(phone_number__isnull=True) | Q(phone_number='') |
        Q(latitude__isnull=True) | Q(longitude__isnull=True)
    )
    targets = list(
        TelegramUser.objects.filter(is_active=True).filter(incomplete)
        .only('id', 'telegram_id', 'language')
    )
    log.total = len(targets)
    log.save(update_fields=['total'])

    if not targets:
        log.status = 'completed'
        log.completed_at = timezone.now()
        log.save(update_fields=['status', 'completed_at'])
        return {'sent': 0, 'failed': 0, 'total': 0}

    # Готовим картинку (если есть) — копируем во временный файл для aiogram.
    photo_path = None
    if settings_obj.image:
        try:
            with settings_obj.image.open('rb') as src:
                ext = os.path.splitext(settings_obj.image.name)[1] or '.jpg'
                with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
                    tmp.write(src.read())
                    photo_path = tmp.name
        except Exception as e:
            logger.warning('monthly_reminder: не удалось открыть картинку: %s', e)

    text_uz = settings_obj.text_uz_latin or ''
    text_ru = settings_obj.text_ru or ''

    async def _send_all():
        bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
        sent, failed = 0, 0
        try:
            for i, user in enumerate(targets):
                text = text_ru if user.language == 'ru' else text_uz
                ok, _err = await send_message_to_user(
                    bot=bot, user=user, text=text,
                    parse_mode='HTML', photo_path=photo_path,
                    disable_link_preview=True,
                )
                if ok:
                    sent += 1
                else:
                    failed += 1
                if i < len(targets) - 1:
                    await asyncio.sleep(TELEGRAM_MESSAGE_DELAY)
            return sent, failed
        finally:
            await bot.session.close()

    try:
        sent, failed = asyncio.run(_send_all())
        log.sent_count = sent
        log.failed_count = failed
        log.status = 'completed'
        log.completed_at = timezone.now()
        log.save(update_fields=['sent_count', 'failed_count', 'status', 'completed_at'])
        logger.info(
            'monthly_reminder %s: отправлено %s, ошибок %s из %s',
            month_key, sent, failed, len(targets),
        )
        return {'sent': sent, 'failed': failed, 'total': len(targets)}
    except Exception as e:
        log.status = 'failed'
        log.error_message = str(e)
        log.completed_at = timezone.now()
        log.save(update_fields=['status', 'error_message', 'completed_at'])
        logger.exception('monthly_reminder: ошибка при отправке')
        raise
    finally:
        if photo_path and os.path.exists(photo_path):
            try:
                os.unlink(photo_path)
            except OSError:
                pass


@shared_task(bind=True)
def dispatch_scheduled_region_messages(self):
    """
    Beat-сканер: ищет отложенные региональные рассылки, у которых наступило время,
    и переводит их в очередь Celery. Источник правды — БД, поэтому переживает
    перезапуск Redis/воркеров.

    Атомарный переход pending → running через UPDATE ... WHERE status='pending'
    исключает двойную постановку при одновременной работе нескольких beat'ов.
    """
    from .models import RegionMessageLog

    now = timezone.now()
    pending = RegionMessageLog.objects.filter(
        status='pending',
        scheduled_at__lte=now,
    ).order_by('scheduled_at').values(
        'id', 'region_code', 'message_text', 'image_storage_path',
        'user_type_filter', 'language_filter',
    )

    dispatched = 0
    for row in pending:
        # Атомарный захват: побеждает первый, у кого UPDATE затронул строку.
        claimed = RegionMessageLog.objects.filter(
            id=row['id'], status='pending'
        ).update(status='running')
        if not claimed:
            continue
        send_region_message_task.delay(
            log_id=row['id'],
            region_code=row['region_code'],
            message_text=row['message_text'] or '',
            image_storage_path=row['image_storage_path'] or '',
            user_type_filter=row['user_type_filter'] or None,
            language_filter=row['language_filter'] or None,
        )
        dispatched += 1
        logger.info('Запущена отложенная региональная рассылка id=%s', row['id'])

    return {'dispatched': dispatched, 'checked_at': now.isoformat()}


@shared_task(bind=True, soft_time_limit=600)
def daily_db_backup(self):
    """Har kuni 04:00 da pg_dump → Telegram channel.

    Settings.BACKUP_CHANNEL_ID kerak. Aks holda task silent skip.
    """
    from django.core.management import call_command
    from django.conf import settings
    import io

    if not getattr(settings, 'BACKUP_CHANNEL_ID', ''):
        logger.info("daily_db_backup: BACKUP_CHANNEL_ID sozlanmagan — skip")
        return {'status': 'skipped', 'reason': 'no_channel_id'}

    out = io.StringIO()
    err = io.StringIO()
    try:
        call_command('backup_db', stdout=out, stderr=err)
        logger.info("daily_db_backup OK: %s", out.getvalue())
        return {'status': 'ok'}
    except Exception as exc:
        logger.exception("daily_db_backup failed")
        return {'status': 'error', 'error': str(exc)}
