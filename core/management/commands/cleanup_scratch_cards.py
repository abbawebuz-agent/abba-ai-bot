"""Skretch-kartalarni (QRCode) tozalash — faqat belgilangan oraliqni qoldirish.

Talab (2026-06-04, @Kobiljonovs): admin paneldagi skretch-kartalardan FAQAT
2-iyunda yaratilgan 00000001 .. 00000811 (global tartib raqami) oralig'idagilar
qolsin, qolganlari o'chirilsin.

Qoldiriladi:  sequence_number  --keep-from .. --keep-to  oralig'ida (default 1..811)
O'chiriladi:  shu oraliqdan tashqaridagi BARCHA QRCode (sequence_number > 811,
              shuningdek sequence_number IS NULL bo'lgan eski/buzuq yozuvlar).

QRCode'ga bog'liq yozuvlar CASCADE bilan o'zi o'chadi:
    - MonthlyPromoTicket (OneToOne, CASCADE)
    - QRCodeScanAttempt (FK, CASCADE)

Standart holatda DRY-RUN: nima o'chishini sanab ko'rsatadi, lekin o'chirmaydi.
Haqiqatan o'chirish uchun:
    python manage.py cleanup_scratch_cards --confirm
Oraliqni o'zgartirish:
    python manage.py cleanup_scratch_cards --keep-from 1 --keep-to 811 --confirm
"""
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Q

from core.models import QRCode


class Command(BaseCommand):
    help = (
        "Belgilangan sequence_number oralig'idan (default 1..811) tashqaridagi "
        "barcha skretch-kartalarni (QRCode) o'chiradi. Default: dry-run."
    )

    def add_arguments(self, parser):
        parser.add_argument('--keep-from', type=int, default=1,
                            help='Qoldiriladigan eng kichik tartib raqami (default: 1).')
        parser.add_argument('--keep-to', type=int, default=811,
                            help='Qoldiriladigan eng katta tartib raqami (default: 811).')
        parser.add_argument('--confirm', action='store_true',
                            help="Haqiqatan o'chirish. Bo'lmasa faqat dry-run.")

    def handle(self, *args, **options):
        keep_from = options['keep_from']
        keep_to = options['keep_to']
        confirm = options['confirm']

        keep_qs = QRCode.objects.filter(sequence_number__range=(keep_from, keep_to))
        # O'chiriladiganlar: oraliqdan tashqari YOKI sequence_number yo'q (NULL)
        delete_qs = QRCode.objects.filter(
            ~Q(sequence_number__range=(keep_from, keep_to)) | Q(sequence_number__isnull=True)
        )

        total = QRCode.objects.count()
        keep_cnt = keep_qs.count()
        del_cnt = delete_qs.count()

        self.stdout.write(self.style.MIGRATE_HEADING(
            '\n=== Skretch-kartalarni tozalash ==='
        ))
        self.stdout.write('Rejim: ' + (
            self.style.ERROR("HAQIQIY O'CHIRISH (--confirm)") if confirm
            else self.style.WARNING("DRY-RUN (hech narsa o'chmaydi)")
        ))
        self.stdout.write(
            f"\nQoldiriladi: sequence_number {keep_from}..{keep_to}  "
            f"-> {self.style.SUCCESS(str(keep_cnt))} ta"
        )
        self.stdout.write(
            f"O'chiriladi: oraliqdan tashqari + NULL  "
            f"-> {self.style.NOTICE(str(del_cnt))} ta"
        )
        self.stdout.write(f"Jami hozir: {total} ta skretch-karta")

        # Skanerlangan kartalar bormi (o'chsa ball tarixi ham CASCADE ketadi) — ogohlantirish
        scanned_del = delete_qs.filter(is_scanned=True).count()
        if scanned_del:
            self.stdout.write(self.style.WARNING(
                f"\n⚠️  Diqqat: o'chiriladiganlar ichida {scanned_del} ta ALLAQACHON "
                f"SKANERLANGAN karta bor (ular bilan birga monthly_ticket/skan tarixi ham o'chadi)."
            ))

        if not confirm:
            self.stdout.write(self.style.WARNING(
                f"\n[DRY-RUN] {del_cnt} ta karta o'chiriladi, {keep_cnt} ta qoladi.\n"
                f"Haqiqatan o'chirish uchun:\n"
                f"    python manage.py cleanup_scratch_cards "
                f"--keep-from {keep_from} --keep-to {keep_to} --confirm\n"
            ))
            return

        self.stdout.write(self.style.ERROR("\nO'chirilmoqda..."))
        with transaction.atomic():
            n, per_model = delete_qs.delete()
        self.stdout.write(self.style.SUCCESS(
            f"\n✅ Tugadi. O'chdi: {n} qator (cascade bilan). "
            f"Qoldi: {QRCode.objects.count()} ta skretch-karta."
        ))
        for model_label, cnt in sorted(per_model.items()):
            self.stdout.write(f"  - {model_label}: {cnt}")
