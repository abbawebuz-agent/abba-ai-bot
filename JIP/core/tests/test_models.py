"""
Model logikasi uchun unit testlar.
"""
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.utils import timezone

from core.models import (
    Gift,
    GiftRedemption,
    QRCode,
    QRCodeBatch,
    SellerPointsTransaction,
    Store,
    TelegramUser,
    UzRegion,
)


class TelegramUserTests(TestCase):
    def setUp(self):
        self.region = UzRegion.objects.create(code='TST', name_uz='Test', name_ru='Тест')

    def _make_user(self, **kwargs):
        defaults = {
            'telegram_id': 123456,
            'first_name': 'Test',
            'phone_number': '+998901234567',
            'user_type': TelegramUser.USER_TYPE_SANTENIK,
            'region': self.region,
        }
        defaults.update(kwargs)
        return TelegramUser.objects.create(**defaults)

    def test_is_promo_code_blocked_returns_false_when_not_blocked(self):
        user = self._make_user()
        blocked, _stage, _until = user.is_promo_code_blocked()
        self.assertFalse(blocked)

    def test_is_promo_code_blocked_true_when_future_block(self):
        user = self._make_user(promo_blocked_until=timezone.now() + timedelta(hours=1))
        blocked, _stage, until = user.is_promo_code_blocked()
        self.assertTrue(blocked)
        self.assertIsNotNone(until)

    def test_is_promo_code_blocked_false_when_past_block(self):
        user = self._make_user(promo_blocked_until=timezone.now() - timedelta(hours=1))
        blocked, _stage, _until = user.is_promo_code_blocked()
        self.assertFalse(blocked)

    @override_settings(PROMO_MAX_INVALID_ATTEMPTS=3, PROMO_BLOCK_DURATION_HOURS=24)
    def test_register_invalid_attempt_blocks_after_threshold(self):
        user = self._make_user()
        for _ in range(2):
            user.register_invalid_promo_attempt('bot', 'BAD')
            user.refresh_from_db()
        self.assertFalse(user.is_promo_code_blocked()[0])
        user.register_invalid_promo_attempt('bot', 'BAD')
        user.refresh_from_db()
        self.assertTrue(user.is_promo_code_blocked()[0])
        self.assertEqual(user.promo_block_stage, 1)
        # Counter 0 ga tushgan bo'lishi kerak
        self.assertEqual(user.promo_failed_attempts, 0)

    def test_register_successful_promo_resets_counter(self):
        user = self._make_user(promo_failed_attempts=2)
        user.register_successful_promo('OK', 'bot')
        user.refresh_from_db()
        self.assertEqual(user.promo_failed_attempts, 0)
        self.assertIsNone(user.promo_blocked_until)

    def test_full_name(self):
        user = self._make_user(first_name='Ali', last_name='Valiyev')
        self.assertEqual(user.full_name, 'Ali Valiyev')


class StoreAndBatchTests(TestCase):
    def setUp(self):
        self.region = UzRegion.objects.create(code='TAS', name_uz='Toshkent', name_ru='Ташкент')
        self.seller = TelegramUser.objects.create(
            telegram_id=99,
            user_type=TelegramUser.USER_TYPE_SOTUVCHI,
            phone_number='+998900000000',
        )
        self.store = Store.objects.create(
            name='JIP Bozor 1',
            phone='+998999998877',
            address='Toshkent, Yunusobod',
            region=self.region,
            owner=self.seller,
        )

    def test_store_str(self):
        self.assertEqual(str(self.store), 'JIP Bozor 1')

    def test_batch_creation_and_activation_rate(self):
        batch = QRCodeBatch.objects.create(
            name='TEST-001', store=self.store, quantity=10, points_per_code=50,
        )
        # Initial — 0 ta QR
        self.assertEqual(batch.activation_rate(), 0)

        # 4 ta QR yaratamiz, 2 tasi skanlangan
        for i in range(4):
            QRCode.objects.create(
                code=f'C{i:04d}', hash_code=f'H{i:04d}', serial_number=f'SN{i:04d}',
                points=50, store=self.store, batch=batch,
                is_scanned=(i < 2),
                scanned_at=timezone.now() if i < 2 else None,
            )
        # Quantity 10 da 2 ta scanned = 20%
        self.assertEqual(batch.activation_rate(), 20.0)


class SellerBalanceTests(TestCase):
    def setUp(self):
        self.region = UzRegion.objects.create(code='X', name_uz='X', name_ru='X')
        self.seller = TelegramUser.objects.create(
            telegram_id=1,
            user_type=TelegramUser.USER_TYPE_SOTUVCHI,
            phone_number='+998901111111',
        )
        self.store = Store.objects.create(
            name='S', phone='+998999998877', address='A', region=self.region, owner=self.seller,
        )

    def test_seller_calculate_points_sums_transactions(self):
        SellerPointsTransaction.objects.create(seller=self.seller, store=self.store, points=100)
        SellerPointsTransaction.objects.create(seller=self.seller, store=self.store, points=50)
        SellerPointsTransaction.objects.create(seller=self.seller, store=self.store, points=-20)
        self.assertEqual(self.seller.calculate_points(force=True), 130)


class SantenikBalanceTests(TestCase):
    def setUp(self):
        self.region = UzRegion.objects.create(code='X', name_uz='X', name_ru='X')
        self.owner = TelegramUser.objects.create(
            telegram_id=1, user_type=TelegramUser.USER_TYPE_SOTUVCHI, phone_number='+99800',
        )
        self.store = Store.objects.create(
            name='S', phone='+99811', address='A', region=self.region, owner=self.owner,
        )
        self.santenik = TelegramUser.objects.create(
            telegram_id=2, user_type=TelegramUser.USER_TYPE_SANTENIK, phone_number='+99822',
        )
        self.batch = QRCodeBatch.objects.create(name='B', store=self.store, quantity=10, points_per_code=50)

    def _make_qr(self, code: str, points: int = 50, scanned_by=None):
        return QRCode.objects.create(
            code=code, hash_code=code.lower(), serial_number='S' + code,
            points=points, store=self.store, batch=self.batch,
            is_scanned=scanned_by is not None, scanned_by=scanned_by,
            scanned_at=timezone.now() if scanned_by else None,
        )

    def test_santenik_balance_from_scanned_qrs(self):
        self._make_qr('A', 50, scanned_by=self.santenik)
        self._make_qr('B', 100, scanned_by=self.santenik)
        self._make_qr('C', 75, scanned_by=None)  # not scanned by us
        self.assertEqual(self.santenik.calculate_points(force=True), 150)

    def test_santenik_balance_subtracts_redemptions(self):
        self._make_qr('A', 200, scanned_by=self.santenik)
        gift = Gift.objects.create(name_uz_latin='G', points_cost=80, image='dummy.png')
        GiftRedemption.objects.create(user=self.santenik, gift=gift)
        self.assertEqual(self.santenik.calculate_points(force=True), 120)


class UtilsTests(TestCase):
    def test_generate_hash_excludes_confusing_chars(self):
        from core.utils import generate_hash
        for _ in range(100):
            h = generate_hash(10)
            self.assertNotIn('0', h)
            self.assertNotIn('O', h)
            self.assertNotIn('1', h)
            self.assertNotIn('I', h)
            self.assertEqual(len(h), 10)

    def test_generate_serial_format(self):
        from core.utils import generate_serial
        self.assertEqual(generate_serial(5, 12, 100), 'S0005B0012N00100')


class WebAppAuthTests(TestCase):
    @override_settings(TELEGRAM_BOT_TOKEN='123:fake')
    def test_invalid_hash_rejected(self):
        from core.webapp_auth import verify_init_data
        bad = 'user=%7B%22id%22%3A1%7D&auth_date=1234567890&hash=deadbeef'
        self.assertIsNone(verify_init_data(bad))

    @override_settings(TELEGRAM_BOT_TOKEN='')
    def test_missing_token_returns_none(self):
        from core.webapp_auth import verify_init_data
        self.assertIsNone(verify_init_data('any'))
