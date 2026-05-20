"""
QR scan business logikasi testlari.
"""
from django.test import TestCase, override_settings
from django.utils import timezone

from bot.services import _scan_qr_code_sync
from core.models import (
    MonthlyPromoTicket,
    QRCode,
    QRCodeBatch,
    Store,
    TelegramUser,
    UzRegion,
)


class ScanQRCodeTests(TestCase):
    def setUp(self):
        self.region = UzRegion.objects.create(code='X', name_uz='X', name_ru='X')
        self.owner = TelegramUser.objects.create(
            telegram_id=1, user_type=TelegramUser.USER_TYPE_SOTUVCHI, phone_number='+1',
        )
        self.store = Store.objects.create(
            name='Store A', phone='+1', address='A', region=self.region, owner=self.owner,
        )
        self.batch = QRCodeBatch.objects.create(
            name='B-1', store=self.store, quantity=10, points_per_code=50,
        )
        self.santenik = TelegramUser.objects.create(
            telegram_id=2, user_type=TelegramUser.USER_TYPE_SANTENIK, phone_number='+2',
        )
        self.qr = QRCode.objects.create(
            code='ABC123', hash_code='abc123', serial_number='SN1',
            points=50, store=self.store, batch=self.batch,
        )

    def test_successful_scan(self):
        result = _scan_qr_code_sync(self.santenik.pk, 'ABC123', 'bot')
        self.assertEqual(result.status, 'success')
        self.assertEqual(result.points, 50)
        self.assertEqual(result.store_name, 'Store A')
        self.assertEqual(result.balance, 50)

        self.qr.refresh_from_db()
        self.assertTrue(self.qr.is_scanned)
        self.assertEqual(self.qr.scanned_by_id, self.santenik.pk)
        self.assertEqual(MonthlyPromoTicket.objects.count(), 1)

    def test_scan_with_hash_code(self):
        result = _scan_qr_code_sync(self.santenik.pk, 'abc123', 'bot')
        self.assertEqual(result.status, 'success')

    def test_scan_already_used(self):
        self.qr.is_scanned = True
        self.qr.save()
        result = _scan_qr_code_sync(self.santenik.pk, 'ABC123', 'bot')
        self.assertEqual(result.status, 'used')

    def test_scan_invalid_code(self):
        result = _scan_qr_code_sync(self.santenik.pk, 'NOTREAL', 'bot')
        self.assertEqual(result.status, 'invalid')

    def test_scan_wrong_role(self):
        self.owner.user_type = TelegramUser.USER_TYPE_SOTUVCHI
        self.owner.save()
        result = _scan_qr_code_sync(self.owner.pk, 'ABC123', 'bot')
        self.assertEqual(result.status, 'wrong_role')

    def test_scan_blocked_user(self):
        from datetime import timedelta
        self.santenik.promo_blocked_until = timezone.now() + timedelta(hours=1)
        self.santenik.save()
        result = _scan_qr_code_sync(self.santenik.pk, 'ABC123', 'bot')
        self.assertEqual(result.status, 'blocked')

    @override_settings(PROMO_MAX_INVALID_ATTEMPTS=3)
    def test_three_invalid_attempts_blocks(self):
        for _ in range(3):
            _scan_qr_code_sync(self.santenik.pk, 'WRONG', 'bot')
            self.santenik.refresh_from_db()
        self.assertTrue(self.santenik.is_promo_code_blocked()[0])
