"""Barcha test ma'lumotlarini o'chiradi (loyiha PRODUCTION uchun toza bo'lsin).

Faqat aniq test markerlari bo'yicha o'chiradi — real ma'lumotga tegmaydi:
  - Store / QRCodeBatch nomi '[TEST]' bilan boshlanadi
  - TelegramUser username 'testuser' bilan boshlanadi
  - GiftRedemption admin_notes = 'Test ariza — seed_test_data'

Idempotent — qayta-qayta ishlatish xavfsiz (deployda har safar ishlasa ham).
"""
from django.core.management.base import BaseCommand
from django.db import transaction

from core.models import (
    TelegramUser, Store, QRCodeBatch, QRCode,
    SellerPointsTransaction, GiftRedemption,
)


class Command(BaseCommand):
    help = "Barcha [TEST]/testuser test ma'lumotlarini o'chiradi (production tozalash)"

    def handle(self, *args, **options):
        report = {}

        def _del(qs_factory, label):
            # Har bir o'chirish ALOHIDA atomic — biri xato bersa, boshqasi
            # buzilmaydi (Django "transaction is aborted" gotcha'sidan qochish).
            try:
                with transaction.atomic():
                    qs = qs_factory()
                    n = qs.count()
                    if n:
                        qs.delete()
                report[label] = n
            except Exception as e:
                report[label] = f'xato: {e}'

        # Tartib MUHIM: QRCode.batch = PROTECT, shuning uchun avval QR kodlar.
        # 1) Test redemption'lar (testuser yoki seed izohi)
        _del(lambda: GiftRedemption.objects.filter(admin_notes='Test ariza — seed_test_data'),
             'gift_redemptions(seed)')
        _del(lambda: GiftRedemption.objects.filter(user__username__startswith='testuser'),
             'gift_redemptions(testuser)')

        # 2) Sotuvchi ball tranzaksiyalari (test do'kon yoki test sotuvchi bo'yicha)
        _del(lambda: SellerPointsTransaction.objects.filter(store__name__startswith='[TEST]'),
             'seller_txns(store)')
        _del(lambda: SellerPointsTransaction.objects.filter(seller__username__startswith='testuser'),
             'seller_txns(seller)')

        # 3) QR kodlar (test batch yoki test do'kon) — batch'dan OLDIN (PROTECT)
        _del(lambda: QRCode.objects.filter(batch__name__startswith='[TEST]'),
             'qrcodes(batch)')
        _del(lambda: QRCode.objects.filter(store__name__startswith='[TEST]'),
             'qrcodes(store)')

        # 4) Partiyalar (Promokod yaratish tarixi)
        _del(lambda: QRCodeBatch.objects.filter(name__startswith='[TEST]'), 'batches')

        # 5) Test do'konlar
        _del(lambda: Store.objects.filter(name__startswith='[TEST]'), 'stores')

        # 6) Test foydalanuvchilar (testuser*)
        _del(lambda: TelegramUser.objects.filter(username__startswith='testuser'), 'users(testuser)')

        self.stdout.write(self.style.SUCCESS(
            'Test ma\'lumotlari tozalandi: ' + ', '.join(f'{k}={v}' for k, v in report.items())
        ))
