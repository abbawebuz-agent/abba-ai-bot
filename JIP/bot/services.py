"""
Bot business logic — sync DB operations wrapped via `asgiref.sync_to_async`.

Bot ishlatadigan hamma DB operatsiyalari shu yerda. aiogram async,
Django ORM esa default'da sync — shuning uchun sinx_to_async ishlatamiz.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional

from asgiref.sync import sync_to_async
from django.conf import settings
from django.db import transaction
from django.db.models import Max, Q
from django.utils import timezone

from core.models import (
    MonthlyPromoTicket,
    QRCode,
    Store,
    TelegramUser,
)


# ---------------------------------------------------------------------------
# User helpers
# ---------------------------------------------------------------------------

@sync_to_async
def get_or_create_user(telegram_id: int, **defaults) -> tuple[TelegramUser, bool]:
    user, created = TelegramUser.objects.get_or_create(
        telegram_id=telegram_id,
        defaults=defaults,
    )
    return user, created


@sync_to_async
def update_user_fields(user_id: int, **fields) -> None:
    TelegramUser.objects.filter(pk=user_id).update(**fields)


@sync_to_async
def get_user_by_telegram_id(telegram_id: int) -> Optional[TelegramUser]:
    return TelegramUser.objects.filter(telegram_id=telegram_id).first()


@sync_to_async
def find_store_for_seller(phone_number: str, seller_user_id: int) -> Optional[Store]:
    """Sotuvchi ro'yxatdan o'tganda — telefon raqami orqali Store qidiramiz."""
    if not phone_number:
        return None
    normalized = ''.join(ch for ch in phone_number if ch.isdigit() or ch == '+')
    candidates = Store.objects.filter(is_active=True).filter(
        Q(phone__contains=normalized[-9:]) | Q(owner_id=seller_user_id)
    ).select_related('region', 'district').first()
    return candidates


@sync_to_async
def link_seller_to_store(user_id: int, store_id: int) -> None:
    """Sotuvchi do'kon egasi sifatida belgilanadi."""
    Store.objects.filter(pk=store_id).update(owner_id=user_id)


# ---------------------------------------------------------------------------
# QR scan logic — TZ §6.5
# ---------------------------------------------------------------------------

@dataclass
class ScanResult:
    status: str  # 'success' | 'invalid' | 'used' | 'blocked' | 'wrong_role'
    points: int = 0
    balance: int = 0
    store_name: str = ''
    blocked_until: Optional[datetime] = None


def _next_global_order() -> int:
    last = MonthlyPromoTicket.objects.aggregate(m=Max('order'))['m'] or 0
    return last + 1


def _month_start(dt: datetime) -> date:
    return date(dt.year, dt.month, 1)


def _scan_qr_code_sync(user_pk: int, raw_code: str, source: str) -> ScanResult:
    """Synchronous QR scan — ScanResult qaytaradi. TZ §6.5."""
    user = TelegramUser.objects.select_for_update().get(pk=user_pk)

    blocked, _stage, blocked_until = user.is_promo_code_blocked()
    if blocked:
        return ScanResult(status='blocked', blocked_until=blocked_until)

    if user.user_type != TelegramUser.USER_TYPE_SANTENIK:
        return ScanResult(status='wrong_role')

    code_normalized = (raw_code or '').upper().strip()
    if not code_normalized:
        user.register_invalid_promo_attempt(source, raw_code)
        return ScanResult(status='invalid')

    try:
        qr = QRCode.objects.select_for_update().select_related('store').get(
            Q(code__iexact=code_normalized) | Q(hash_code__iexact=code_normalized),
            is_deleted=False,
        )
    except QRCode.DoesNotExist:
        user.register_invalid_promo_attempt(source, raw_code)
        return ScanResult(status='invalid')

    if qr.is_scanned:
        user.register_invalid_promo_attempt(source, raw_code)
        return ScanResult(status='used')

    now = timezone.now()
    qr.is_scanned = True
    qr.scanned_at = now
    qr.scanned_by = user
    qr.save(update_fields=['is_scanned', 'scanned_at', 'scanned_by'])

    MonthlyPromoTicket.objects.create(
        month=_month_start(now),
        qr_code=qr,
        user=user,
        store=qr.store,
        order=_next_global_order(),
        scanned_at=now,
    )

    user.register_successful_promo(raw_code, source)
    user.invalidate_points_cache()
    new_balance = user.calculate_points(force=True)

    return ScanResult(
        status='success',
        points=qr.points,
        balance=new_balance,
        store_name=qr.store.name,
    )


@sync_to_async
def scan_qr_code(user_pk: int, raw_code: str, source: str = 'bot') -> ScanResult:
    with transaction.atomic():
        return _scan_qr_code_sync(user_pk, raw_code, source)


# ---------------------------------------------------------------------------
# Balance
# ---------------------------------------------------------------------------

@sync_to_async
def get_user_balance(user_pk: int) -> int:
    user = TelegramUser.objects.get(pk=user_pk)
    return user.calculate_points()


# ---------------------------------------------------------------------------
# Support contact
# ---------------------------------------------------------------------------

def support_contact() -> str:
    return getattr(settings, 'SUPPORT_TELEGRAM', '@jip_support')
