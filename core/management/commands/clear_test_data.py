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

        def _del(qs, label):
            try:
                n = qs.count()
                if n:
                    qs.delete()
                report[label] = n
            except Exception as e:
                report[label] = f'xato: {e}'

        with transaction.atomic():
            test_stores = Store.objects.filter(name__startswith='[TEST]')
            test_batches = QRCodeBatch.objects.filter(name__startswith='[TEST]')
            test_users = TelegramUser.objects.filter(username__startswith='testuser')

            # Tartib MUHIM: QRCode.batch = PROTECT, shuning uchun avval QR kodlar.
            # 1) Test redemption'lar (testuser yoki seed izohi)
            _del(GiftRedemption.objects.filter(admin_notes='Test ariza — seed_test_data'),
                 'gift_redemptions(seed)')
            _del(GiftRedemption.objects.filter(user__username__startswith='testuser'),
                 'gift_redemptions(testuser)')

            # 2) Sotuvchi ball tranzaksiyalari (test do'kon bo'yicha)
            _del(SellerPointsTransaction.objects.filter(store__name__startswith='[TEST]'),
                 'seller_txns(store)')
            _del(SellerPointsTransaction.objects.filter(seller__username__startswith='testuser'),
                 'seller_txns(seller)')

            # 3) QR kodlar (test batch yoki test do'kon) — batch'dan OLDIN (PROTECT)
            _del(QRCode.objects.filter(batch__name__startswith='[TEST]'),
                 'qrcodes(batch)')
            _del(QRCode.objects.filter(store__name__startswith='[TEST]'),
                 'qrcodes(store)')

            # 4) Partiyalar (Promokod yaratish tarixi)
            _del(test_batches, 'batches')

            # 5) Test do'konlar
            _del(test_stores, 'stores')

            # 6) Test foydalanuvchilar (testuser*)
            _del(test_users, 'users(testuser)')

        self.stdout.write(self.style.SUCCESS(
            'Test ma\'lumotlari tozalandi: ' + ', '.join(f'{k}={v}' for k, v in report.items())
        ))
