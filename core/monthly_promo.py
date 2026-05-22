"""
Месячный розыгрыш: каждый отсканированный промокод = билет с порядковым № в месяце.
"""

from __future__ import annotations

from datetime import date, datetime

from django.db import transaction
from django.db.models import Max

from .models import MonthlyPromoTicket, QRCode, TelegramUser


def month_start(dt: datetime | date) -> date:
    if isinstance(dt, datetime):
        dt = dt.date()
    return date(dt.year, dt.month, 1)


def assign_monthly_ticket(*, qr_code: QRCode, user: TelegramUser) -> MonthlyPromoTicket:
    """
    Создаёт билет (MonthlyPromoTicket) для отсканированного QR-кода.
    Идемпотентен по qr_code: если билет уже выдан — возвращает существующий.

    `order` — следующий свободный № внутри (month, user_type), вычисляется
    под `select_for_update`, чтобы при параллельных сканированиях номера
    шли подряд без коллизий.
    """
    scanned_at = qr_code.scanned_at
    if scanned_at is None:
        raise ValueError('assign_monthly_ticket: qr_code.scanned_at is None')

    m = month_start(scanned_at)
    ut = user.user_type or 'electrician'

    with transaction.atomic():
        existing = (
            MonthlyPromoTicket.objects.select_for_update()
            .filter(qr_code=qr_code)
            .first()
        )
        if existing:
            return existing

        last_order = (
            MonthlyPromoTicket.objects.select_for_update()
            .filter(user_type=ut)
            .aggregate(v=Max('order'))
            .get('v')
        ) or 0

        return MonthlyPromoTicket.objects.create(
            month=m,
            qr_code=qr_code,
            user=user,
            user_type=ut,
            order=last_order + 1,
            scanned_at=scanned_at,
        )


def count_user_chances(*, user: TelegramUser, when: datetime | date | None = None) -> int:
    """
    Сколько шансов (билетов) у пользователя в указанном месяце.
    По умолчанию — текущий месяц (по локальному времени сервера).
    Игнорирует билеты на удалённых QR-кодах — чтобы счётчик совпадал с тем,
    что юзер видит в истории.
    """
    if when is None:
        from django.utils import timezone
        when = timezone.localtime(timezone.now())
    m = month_start(when)
    return MonthlyPromoTicket.objects.filter(
        user=user,
        month=m,
        qr_code__is_deleted=False,
    ).count()
