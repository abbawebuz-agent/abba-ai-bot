"""
Бэкфилл MonthlyPromoTicket из исторических сканов QRCode.

Для каждого scanned_at-отсортированного QRCode (is_scanned=True, scanned_by IS NOT NULL)
создаём ticket с порядковым № внутри (month, user_type). Идемпотентен: если для qr
билет уже есть, скан пропускается.
"""

from collections import defaultdict
from datetime import date

from django.db import migrations
from django.utils import timezone


def _month_start(d):
    if hasattr(d, 'date'):
        d = d.date()
    return date(d.year, d.month, 1)


def backfill(apps, schema_editor):
    QRCode = apps.get_model('core', 'QRCode')
    Ticket = apps.get_model('core', 'MonthlyPromoTicket')

    from django.db.models import Max

    existing_qr_ids = set(Ticket.objects.values_list('qr_code_id', flat=True))
    counters = defaultdict(int)
    for row in Ticket.objects.values('month', 'user_type').annotate(max_order=Max('order')):
        counters[(row['month'], row['user_type'])] = row['max_order'] or 0

    batch = []
    qs = (
        QRCode.objects.filter(
            is_scanned=True,
            scanned_by__isnull=False,
            scanned_at__isnull=False,
        )
        .order_by('scanned_at', 'id')
        .iterator(chunk_size=500)
    )
    for qr in qs:
        if qr.id in existing_qr_ids:
            continue
        ut = (getattr(qr.scanned_by, 'user_type', None) or 'electrician')
        m = _month_start(timezone.localtime(qr.scanned_at))
        counters[(m, ut)] += 1
        batch.append(Ticket(
            month=m,
            qr_code_id=qr.id,
            user_id=qr.scanned_by_id,
            user_type=ut,
            order=counters[(m, ut)],
            scanned_at=qr.scanned_at,
        ))
        if len(batch) >= 1000:
            Ticket.objects.bulk_create(batch)
            batch = []
    if batch:
        Ticket.objects.bulk_create(batch)


def noop(apps, schema_editor):
    """Откат: не делаем (билеты безопаснее не трогать)."""
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0057_monthly_promo_ticket'),
    ]

    operations = [
        migrations.RunPython(backfill, reverse_code=noop),
    ]
