"""Foydalanuvchi/test ma'lumotlarini TO'LIQ o'chiradi — FAQAT Sovg'alar (Gift) qoladi.

clear_test_data faqat [TEST]/testuser markerli yozuvlarni o'chiradi. Bot orqali
qo'lda yaratilgan test data (real userlar, partiyalar, sotuvchilar) markersiz
bo'lgani uchun o'chmaydi. Bu komanda esa Gift va reference (UzRegion, admin)
dan tashqari HAMMA ma'lumotni o'chiradi — production'ni toza ishga tushirish uchun.

QOLADI: Gift (sovg'alar), UzRegion, Django auth User (admin), sozlamalar.
O'CHADI: TelegramUser, QRCode, QRCodeBatch, Seller, SellerBatch,
         SellerPointsTransaction, GiftRedemption, MonthlyPromoTicket,
         SellerRegistrationCode, Store.

XAVFSIZLIK: tasodifan ishlamasin uchun --yes SHART. Deployda ishlamaydi.

Usage:
    python manage.py wipe_user_data --yes
"""
from django.core.management.base import BaseCommand
from django.db import transaction

from core.models import (
    TelegramUser, QRCode, QRCodeBatch, GiftRedemption,
    Seller, SellerBatch, SellerPointsTransaction,
    MonthlyPromoTicket, SellerRegistrationCode,
    LiveStreamWinner,
)

try:
    from core.models import Store
except Exception:  # Store olib tashlangan bo'lishi mumkin
    Store = None


class Command(BaseCommand):
    help = "Gift'dan tashqari HAMMA foydalanuvchi/test ma'lumotini o'chiradi"

    def add_arguments(self, parser):
        parser.add_argument('--yes', action='store_true',
                            help="Tasdiq — busiz hech narsa o'chmaydi")

    def handle(self, *args, **opts):
        if not opts['yes']:
            self.stdout.write(self.style.WARNING(
                "⚠️ --yes berilmadi — hech narsa o'chirilmadi (xavfsizlik)."
            ))
            return

        report = {}

        def _del(qs_factory, label):
            # Har biri ALOHIDA atomic — biri xato bersa boshqasi buzilmaydi.
            try:
                with transaction.atomic():
                    qs = qs_factory()
                    n = qs.count()
                    if n:
                        qs.delete()
                report[label] = n
            except Exception as e:
                report[label] = f'xato: {e}'

        # FK PROTECT/CASCADE tartibi muhim: bolalardan ota-onaga.
        _del(lambda: GiftRedemption.objects.all(), 'gift_redemptions')
        # LiveStreamWinner.user -> PROTECT(TelegramUser): userdan OLDIN o'chmasa
        # TelegramUser.delete() ProtectedError beradi va userlar qolib ketadi.
        _del(lambda: LiveStreamWinner.objects.all(), 'livestream_winners')
        _del(lambda: MonthlyPromoTicket.objects.all(), 'monthly_tickets')
        _del(lambda: SellerPointsTransaction.objects.all(), 'seller_txns')
        _del(lambda: SellerBatch.objects.all(), 'seller_batches')
        _del(lambda: QRCode.objects.all(), 'qrcodes')          # batch=PROTECT → batchdan oldin
        _del(lambda: QRCodeBatch.objects.all(), 'batches')
        _del(lambda: Seller.objects.all(), 'sellers')
        _del(lambda: SellerRegistrationCode.objects.all(), 'seller_reg_codes')
        if Store is not None:
            _del(lambda: Store.objects.all(), 'stores')
        _del(lambda: TelegramUser.objects.all(), 'users')

        self.stdout.write(self.style.SUCCESS(
            "Wipe tugadi (Gift qoldi): " + ', '.join(f'{k}={v}' for k, v in report.items())
        ))
