"""
Backfill MonthlyPromoTicket из базы отсканированных QR-кодов.

Логика:
- Берём успешные сканы: QRCode.is_scanned=True, scanned_by IS NOT NULL, scanned_at IS NOT NULL.
- Идём по возрастанию scanned_at — это даёт стабильный исторический порядок order.
- Для каждого скана вычисляем order = (max order в (month, user_type)) + 1.
- Идемпотентен: если для qr_code билет уже есть, скан пропускается.

Опции:
- --dry-run: ничего не пишет, только считает.
- --rebuild: удаляет все существующие тикеты и пересобирает с нуля.
"""

from __future__ import annotations

from collections import defaultdict

from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Max
from django.utils import timezone

from core.models import MonthlyPromoTicket, QRCode
from core.monthly_promo import month_start


class Command(BaseCommand):
    help = "Backfill MonthlyPromoTicket по истории сканов QRCode"

    def add_arguments(self, parser):
        parser.add_argument('--dry-run', action='store_true', help='Только посчитать, не писать.')
        parser.add_argument('--rebuild', action='store_true', help='Удалить все билеты и пересобрать.')

    def handle(self, *args, **options):
        dry_run = bool(options.get('dry_run'))
        rebuild = bool(options.get('rebuild'))

        scans = (
            QRCode.objects.filter(
                is_scanned=True,
                scanned_by__isnull=False,
                scanned_at__isnull=False,
            )
            .select_related('scanned_by')
            .order_by('scanned_at', 'id')
        )

        with transaction.atomic():
            if rebuild:
                deleted = MonthlyPromoTicket.objects.count()
                self.stdout.write(f'Удалить тикетов: {deleted}')
                if not dry_run:
                    MonthlyPromoTicket.objects.all().delete()

            existing_qr_ids: set[int] = (
                set() if rebuild
                else set(MonthlyPromoTicket.objects.values_list('qr_code_id', flat=True))
            )

            # Стартовые order'ы по user_type (глобальный счётчик, не сбрасывается при смене месяца)
            counters: dict[str, int] = defaultdict(int)
            if not rebuild:
                for row in (
                    MonthlyPromoTicket.objects
                    .values('user_type')
                    .annotate(max_order=Max('order'))
                ):
                    counters[row['user_type']] = row['max_order'] or 0

            new_tickets: list[MonthlyPromoTicket] = []
            for qr in scans.iterator(chunk_size=500):
                if qr.id in existing_qr_ids:
                    continue
                user = qr.scanned_by
                ut = (user.user_type if user else None) or 'electrician'
                m = month_start(timezone.localtime(qr.scanned_at))
                counters[ut] += 1
                new_tickets.append(MonthlyPromoTicket(
                    month=m,
                    qr_code_id=qr.id,
                    user_id=user.id,
                    user_type=ut,
                    order=counters[ut],
                    scanned_at=qr.scanned_at,
                ))
                if len(new_tickets) >= 1000 and not dry_run:
                    MonthlyPromoTicket.objects.bulk_create(new_tickets, batch_size=1000)
                    new_tickets = []

            if new_tickets and not dry_run:
                MonthlyPromoTicket.objects.bulk_create(new_tickets, batch_size=1000)

        total = sum(counters.values())
        self.stdout.write(self.style.SUCCESS(f'Готово. Итого тикетов: {total}'))
        if dry_run:
            self.stdout.write(self.style.WARNING('dry-run: записей не внесено.'))
