"""
Экспорт пользователей, заработавших баллы за месяц (по факту сканов QR),
с попытками ввода промокода (PromoCodeAttempt) за тот же месяц.

Пример:
    python manage.py export_user_points_month --year 2026 --month 3 --output-dir ./out
"""
import csv
import os
from datetime import datetime

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.models import Count, Sum
from django.utils import timezone

from core.models import PromoCodeAttempt, QRCode, TelegramUser


class Command(BaseCommand):
    help = (
        "CSV: пользователи с начисленными баллами за месяц (сумма points по сканам QR) "
        "и попытки ввода промокода PromoCodeAttempt (неуспешные, успешные, всего) за тот же период."
    )

    def add_arguments(self, parser):
        parser.add_argument("--year", type=int, default=None, help="Год (по умолчанию — текущий).")
        parser.add_argument("--month", type=int, default=None, help="Месяц 1–12 (по умолчанию — текущий).")
        parser.add_argument(
            "--output-dir",
            type=str,
            default="exports",
            help="Каталог для CSV (по умолчанию: ./exports).",
        )
        parser.add_argument(
            "--output-file",
            type=str,
            default=None,
            help="Имя файла (по умолчанию: users_points_YYYY_MM.csv).",
        )

    def handle(self, *args, **options):
        year = options["year"]
        month = options["month"]
        output_dir = options["output_dir"] or "exports"
        output_file = options["output_file"]

        now = timezone.now()
        if year is None:
            year = now.year
        if month is None:
            month = now.month

        if not (1 <= int(month) <= 12):
            raise SystemExit(self.style.ERROR("month должен быть в диапазоне 1–12"))

        local_tz = timezone.get_current_timezone()
        start_naive = datetime(year=int(year), month=int(month), day=1)
        start = timezone.make_aware(start_naive, local_tz)
        if int(month) == 12:
            end_naive = datetime(year=int(year) + 1, month=1, day=1)
        else:
            end_naive = datetime(year=int(year), month=int(month) + 1, day=1)
        end = timezone.make_aware(end_naive, local_tz)

        os.makedirs(output_dir, exist_ok=True)
        if not output_file:
            output_file = f"users_points_{year}_{int(month):02d}.csv"
        path = os.path.join(output_dir, output_file)

        self.stdout.write(
            self.style.NOTICE(
                f"Период: {year}-{int(month):02d}, TZ={settings.TIME_ZONE} → {path}"
            )
        )

        base_qr = QRCode.objects.filter(
            is_scanned=True,
            is_deleted=False,
            scanned_by__isnull=False,
            scanned_at__gte=start,
            scanned_at__lt=end,
        )

        earned_rows = (
            base_qr.values("scanned_by_id")
            .annotate(points_earned=Sum("points"), scans_count=Count("id"))
            .filter(points_earned__gt=0)
        )
        user_ids = [r["scanned_by_id"] for r in earned_rows]
        earned_map = {r["scanned_by_id"]: r for r in earned_rows}

        fail_rows = (
            PromoCodeAttempt.objects.filter(
                attempted_at__gte=start,
                attempted_at__lt=end,
                is_successful=False,
                user_id__in=user_ids,
            )
            .values("user_id")
            .annotate(n=Count("id"))
        )
        fail_map = {r["user_id"]: r["n"] for r in fail_rows}

        ok_rows = (
            PromoCodeAttempt.objects.filter(
                attempted_at__gte=start,
                attempted_at__lt=end,
                is_successful=True,
                user_id__in=user_ids,
            )
            .values("user_id")
            .annotate(n=Count("id"))
        )
        ok_map = {r["user_id"]: r["n"] for r in ok_rows}

        users = (
            TelegramUser.objects.filter(id__in=user_ids)
            .select_related("region", "district")
            .order_by("-points", "id")
        )

        n = 0
        with open(path, "w", encoding="utf-8", newline="") as f:
            w = csv.writer(f)
            w.writerow(
                [
                    "user_id",
                    "telegram_id",
                    "username",
                    "first_name",
                    "last_name",
                    "phone_number",
                    "user_type",
                    "region_code",
                    "district_code",
                    "points_current",
                    "points_earned_in_month",
                    "qr_scans_in_month",
                    "promo_code_attempts_failed_in_month",
                    "promo_code_attempts_successful_in_month",
                    "promo_code_attempts_total_in_month",
                ]
            )
            for u in users:
                er = earned_map[u.id]
                failed_n = fail_map.get(u.id, 0)
                ok_n = ok_map.get(u.id, 0)
                w.writerow(
                    [
                        u.id,
                        u.telegram_id,
                        u.username or "",
                        u.first_name or "",
                        u.last_name or "",
                        u.phone_number or "",
                        u.user_type or "",
                        u.region.code if u.region_id else "",
                        u.district.code if u.district_id else "",
                        u.points,
                        er["points_earned"],
                        er["scans_count"],
                        failed_n,
                        ok_n,
                        failed_n + ok_n,
                    ]
                )
                n += 1

        self.stdout.write(self.style.SUCCESS(f"Сохранено строк: {n} → {path}"))
