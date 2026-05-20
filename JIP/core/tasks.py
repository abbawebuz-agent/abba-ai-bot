"""
Celery tasks — TZ §10.
"""
from __future__ import annotations

import logging
from datetime import date, timedelta

from celery import shared_task
from django.core.files.base import ContentFile
from django.db import transaction
from django.utils import timezone

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3)
def generate_batch_zip(self, batch_id: int):
    """Batch uchun QR kartalarni generatsiya qiladi va ZIP yaratadi."""
    from core.models import QRCode, QRCodeBatch
    from core.utils import build_batch_zip, generate_unique_hash, generate_serial

    try:
        batch = QRCodeBatch.objects.select_related('store').get(pk=batch_id)
    except QRCodeBatch.DoesNotExist:
        logger.error('Batch %s not found', batch_id)
        return

    if batch.status == QRCodeBatch.STATUS_COMPLETED and batch.zip_file:
        return

    batch.status = QRCodeBatch.STATUS_PROCESSING
    batch.error_message = ''
    batch.save(update_fields=['status', 'error_message'])

    try:
        existing_count = batch.qr_codes.count()
        to_create = max(0, batch.quantity - existing_count)

        with transaction.atomic():
            for n in range(existing_count + 1, existing_count + to_create + 1):
                hash_code = generate_unique_hash(QRCode, 'hash_code', length=8)
                code = generate_unique_hash(QRCode, 'code', length=10)
                serial = generate_serial(batch.store_id, batch.pk, n)
                QRCode.objects.create(
                    code=code,
                    hash_code=hash_code,
                    serial_number=serial,
                    points=batch.points_per_code,
                    store=batch.store,
                    batch=batch,
                )

        zip_bytes = build_batch_zip(batch)
        batch.zip_file.save(f'batch-{batch.pk}.zip', ContentFile(zip_bytes), save=False)
        batch.status = QRCodeBatch.STATUS_COMPLETED
        batch.completed_at = timezone.now()
        batch.save(update_fields=['zip_file', 'status', 'completed_at'])
        logger.info('Batch %s completed: %d codes', batch.pk, batch.quantity)
    except Exception as exc:  # noqa: BLE001
        batch.status = QRCodeBatch.STATUS_FAILED
        batch.error_message = str(exc)[:1000]
        batch.save(update_fields=['status', 'error_message'])
        raise self.retry(exc=exc, countdown=30)


@shared_task
def send_broadcast(broadcast_id: int):
    """Mass-rassilka jo'natish (placeholder — real bot bilan integratsiya kerak)."""
    from core.models import BroadcastMessage, TelegramUser, RegionMessageLog

    try:
        bm = BroadcastMessage.objects.get(pk=broadcast_id)
    except BroadcastMessage.DoesNotExist:
        return

    bm.status = BroadcastMessage.STATUS_SENDING
    bm.started_at = timezone.now()
    bm.save(update_fields=['status', 'started_at'])

    qs = TelegramUser.objects.filter(is_active=True, blocked_bot_at__isnull=True)
    if bm.user_type_filter:
        qs = qs.filter(user_type=bm.user_type_filter)
    if bm.region_filter_id:
        qs = qs.filter(region_id=bm.region_filter_id)
    if bm.store_filter_id:
        qs = qs.filter(owned_stores=bm.store_filter_id)
    if bm.language_filter:
        qs = qs.filter(language=bm.language_filter)

    bm.total_recipients = qs.count()
    bm.save(update_fields=['total_recipients'])

    # Real send — `send_message_to_user.delay(...)` ga ajratiladi
    for user in qs.iterator(chunk_size=200):
        RegionMessageLog.objects.create(broadcast=bm, user=user, is_successful=True)
        bm.sent_count = (bm.sent_count or 0) + 1

    bm.status = BroadcastMessage.STATUS_COMPLETED
    bm.finished_at = timezone.now()
    bm.save(update_fields=['status', 'sent_count', 'finished_at'])


@shared_task
def cleanup_old_attempts():
    """3 oydan eski PromoCodeAttempt'larni o'chirish."""
    from core.models import PromoCodeAttempt
    threshold = timezone.now() - timedelta(days=90)
    deleted, _ = PromoCodeAttempt.objects.filter(attempted_at__lt=threshold).delete()
    logger.info('Cleaned up %d old promo attempts', deleted)


@shared_task
def recalc_user_points(user_id: int):
    """User ballarini qayta hisoblash."""
    from core.models import TelegramUser
    try:
        u = TelegramUser.objects.get(pk=user_id)
    except TelegramUser.DoesNotExist:
        return
    u.invalidate_points_cache()
    u.calculate_points(force=True)


@shared_task
def daily_stats_snapshot():
    """Har kuni 23:55 da statistikani saqlash (placeholder)."""
    from core.models import QRCode, TelegramUser
    today = date.today()
    stats = {
        'date': today.isoformat(),
        'santenik_count': TelegramUser.objects.filter(user_type=TelegramUser.USER_TYPE_SANTENIK).count(),
        'sotuvchi_count': TelegramUser.objects.filter(user_type=TelegramUser.USER_TYPE_SOTUVCHI).count(),
        'qr_total': QRCode.objects.count(),
        'qr_scanned_today': QRCode.objects.filter(scanned_at__date=today).count(),
    }
    logger.info('Daily snapshot: %s', stats)
    return stats


@shared_task
def send_monthly_reminder():
    """Har oy 1-kuni — ro'yxatdan o'tmaganlarga eslatma (placeholder)."""
    from core.models import MonthlyReminderSettings
    s = MonthlyReminderSettings.objects.first()
    if not s or not s.is_enabled:
        return
    logger.info('Monthly reminder triggered')
