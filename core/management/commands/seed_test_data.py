"""QA uchun test ma'lumotlari yaratish."""
import hashlib
import random
import string
from datetime import date, timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone

from core.models import (
    UzRegion, UzDistrict, TelegramUser, Store,
    QRCodeBatch, QRCode, SellerPointsTransaction, Gift, GiftRedemption,
)


def _uid():
    return ''.join(random.choices(string.hexdigits[:16], k=8))


def _code():
    raw = ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))
    hsh = hashlib.md5(raw.encode()).hexdigest()
    return raw, hsh


class Command(BaseCommand):
    help = 'QA uchun test do\'konlar, foydalanuvchilar, batch va QR kodlar yaratadi'

    def add_arguments(self, parser):
        parser.add_argument(
            '--flush', action='store_true',
            help='Oldin yaratilgan test ma\'lumotlarini o\'chirish (username testuser* bo\'lganlar)'
        )

    def handle(self, *args, **options):
        if options['flush']:
            self._flush()
            self.stdout.write(self.style.WARNING('Test ma\'lumotlari o\'chirildi.'))
            return

        regions = self._ensure_regions()
        santeniklar = self._create_santeniklar(regions)
        sotuvchilar = self._create_sotuvchilar(regions)
        stores = self._create_stores(regions, sotuvchilar)
        batches = self._create_batches(stores)
        qrcodes = self._create_qrcodes(batches, santeniklar)
        self._create_seller_txns(sotuvchilar, stores)
        self._create_gifts()
        self._create_redemptions(santeniklar)

        self.stdout.write(self.style.SUCCESS(
            f'\n✅ Test ma\'lumotlari yaratildi:\n'
            f'   Viloyatlar: {len(regions)}\n'
            f'   Santeniklar: {len(santeniklar)}\n'
            f'   Sotuvchilar: {len(sotuvchilar)}\n'
            f'   Do\'konlar:   {len(stores)}\n'
            f'   Batch\'lar:   {len(batches)}\n'
            f'   QR kodlar:   {len(qrcodes)}\n'
        ))

    # ------------------------------------------------------------------
    def _flush(self):
        TelegramUser.objects.filter(username__startswith='testuser').delete()
        Store.objects.filter(name__startswith='[TEST]').delete()

    # ------------------------------------------------------------------
    def _ensure_regions(self):
        data = [
            ('tashkent',    'Toshkent',      'Ташкент'),
            ('samarkand',   'Samarqand',     'Самарканд'),
            ('fergana',     'Farg\'ona',     'Фергана'),
            ('andijan',     'Andijon',       'Андижан'),
            ('namangan',    'Namangan',      'Наманган'),
            ('bukhara',     'Buxoro',        'Бухара'),
            ('kashkadarya', 'Qashqadaryo',   'Кашкадарья'),
            ('surkhandarya','Surxondaryo',   'Сурхандарья'),
            ('khorezm',     'Xorazm',        'Хорезм'),
            ('navoi',       'Navoiy',        'Навои'),
            ('jizzakh',     'Jizzax',        'Джизак'),
            ('syrdarya',    'Sirdaryo',      'Сырдарья'),
            ('karakalpak',  'Qoraqalpog\'on','Каракалпакстан'),
        ]
        regions = []
        for code, name_uz, name_ru in data:
            r, _ = UzRegion.objects.get_or_create(
                code=code,
                defaults={'name_uz': name_uz, 'name_ru': name_ru},
            )
            regions.append(r)

        # Har viloyatga bir tuman qo'shamiz (agar yo'q bo'lsa)
        district_data = [
            ('tashkent',    'yunusabad',  'Yunusobod',   'Юнусабад'),
            ('tashkent',    'chilanzar',  'Chilonzor',   'Чиланзар'),
            ('samarkand',   'samarkand_city', 'Samarqand shahri', 'г.Самарканд'),
            ('fergana',     'fergana_city',   'Farg\'ona shahri', 'г.Фергана'),
            ('andijan',     'andijan_city',   'Andijon shahri',   'г.Андижан'),
        ]
        for r_code, d_code, name_uz, name_ru in district_data:
            try:
                region = UzRegion.objects.get(code=r_code)
                UzDistrict.objects.get_or_create(
                    region=region, code=d_code,
                    defaults={'name_uz': name_uz, 'name_ru': name_ru},
                )
            except UzRegion.DoesNotExist:
                pass

        return regions

    # ------------------------------------------------------------------
    def _create_santeniklar(self, regions, count=15):
        names = [
            ('Alisher', 'Karimov'), ('Bobur', 'Toshmatov'),
            ('Doniyor', 'Yusupov'), ('Eldor', 'Nazarov'),
            ('Firdavs', 'Mirzaev'), ('Hamid', 'Raximov'),
            ('Ilhom', 'Tursunov'), ('Jamshid', 'Xoliqov'),
            ('Komil', 'Askarov'),  ('Lochinbek', 'Sobirov'),
            ('Mansur', 'Qodirov'), ('Nodir', 'Ergashev'),
            ('Otabek', 'Ibragimov'), ('Parviz', 'Sultonov'),
            ('Ravshan', 'Holmatov'),
        ]
        users = []
        for i, (fn, ln) in enumerate(names[:count]):
            tg_id = 1_000_000 + i
            u, created = TelegramUser.objects.get_or_create(
                telegram_id=tg_id,
                defaults={
                    'username': f'testuser_santenik_{i}',
                    'first_name': fn,
                    'last_name': ln,
                    'phone_number': f'+9989{90+i:07d}',
                    'user_type': 'santenik',
                    'points': random.randint(0, 500),
                    'region': random.choice(regions),
                    'language': random.choice(['uz_latin', 'ru']),
                    'privacy_accepted': True,
                    'is_active': True,
                },
            )
            users.append(u)
        return users

    # ------------------------------------------------------------------
    def _create_sotuvchilar(self, regions, count=5):
        names = [
            ('Sarvar', 'Qosimov'), ('Timur', 'Bahromov'),
            ('Ulugbek', 'Mamatov'), ('Vohid', 'Xasanov'),
            ('Zafar', 'Nishonov'),
        ]
        users = []
        for i, (fn, ln) in enumerate(names[:count]):
            tg_id = 2_000_000 + i
            u, _ = TelegramUser.objects.get_or_create(
                telegram_id=tg_id,
                defaults={
                    'username': f'testuser_sotuvchi_{i}',
                    'first_name': fn,
                    'last_name': ln,
                    'phone_number': f'+9998{70+i:07d}',
                    'user_type': 'sotuvchi',
                    'points': random.randint(100, 2000),
                    'region': regions[i % len(regions)],
                    'language': 'uz_latin',
                    'privacy_accepted': True,
                    'is_active': True,
                    'seller_approved': True,
                },
            )
            users.append(u)
        return users

    # ------------------------------------------------------------------
    def _create_stores(self, regions, sotuvchilar, count=5):
        store_data = [
            ('[TEST] Toshkent Santexnika Plus',   'tashkent',    'yunusabad',       '+998712345678', 'Yunusobod, 19-mavze'),
            ('[TEST] Samarqand Suvchilar Markazi','samarkand',   'samarkand_city',  '+998662345678', 'Registon ko\'chasi 5'),
            ('[TEST] Farg\'ona Suvchi Bozori',    'fergana',     'fergana_city',    '+998732345678', 'Markaziy bozor'),
            ('[TEST] Andijon Santexnika Hub',      'andijan',     'andijan_city',    '+998742345678', 'Asaka ko\'chasi 12'),
            ('[TEST] Namangan Tr Markazi',         'namangan',    None,              '+998692345678', 'Do\'stlik 45'),
        ]
        stores = []
        for i, (name, r_code, d_code, phone, addr) in enumerate(store_data[:count]):
            try:
                region = UzRegion.objects.get(code=r_code)
            except UzRegion.DoesNotExist:
                region = regions[0]
            district = None
            if d_code:
                district = UzDistrict.objects.filter(region=region, code=d_code).first()
            owner = sotuvchilar[i % len(sotuvchilar)]
            s, _ = Store.objects.get_or_create(
                name=name,
                defaults={
                    'legal_name': name.replace('[TEST] ', '') + ' MChJ',
                    'phone': phone,
                    'address': addr,
                    'region': region,
                    'district': district,
                    'owner': owner,
                    'commission_percent': round(random.uniform(3.0, 8.0), 2),
                    'contract_signed_at': date.today() - timedelta(days=random.randint(30, 365)),
                    'is_active': True,
                },
            )
            # Mavjud do'konga ham district biriktiramiz (idempotent)
            if district and not s.district_id:
                s.district = district
                s.save(update_fields=['district'])
            stores.append(s)
        return stores

    # ------------------------------------------------------------------
    def _create_batches(self, stores):
        batches = []
        statuses = ['completed', 'completed', 'processing', 'pending']
        delivery = ['delivered', 'shipped', 'not_shipped', 'not_shipped']
        for idx, store in enumerate(stores):
            for b in range(2):
                name = f'{store.name[:20].strip()}-MAY2026-{b+1:03d}'
                batch, _ = QRCodeBatch.objects.get_or_create(
                    name=name,
                    defaults={
                        'store': store,
                        'quantity': random.choice([50, 100, 200]),
                        'points_per_code': random.choice([50, 100, 150]),
                        'status': statuses[(idx + b) % len(statuses)],
                        'delivery_status': delivery[(idx + b) % len(delivery)],
                        'shipped_at': timezone.now() - timedelta(days=random.randint(1, 30)) if b == 0 else None,
                    },
                )
                batches.append(batch)
        return batches

    # ------------------------------------------------------------------
    def _create_qrcodes(self, batches, santeniklar, per_batch=10):
        qrcodes = []
        for batch in batches:
            existing = batch.qr_codes.count()
            if existing >= per_batch:
                qrcodes.extend(list(batch.qr_codes.all()[:per_batch]))
                continue
            for _ in range(per_batch - existing):
                raw, hsh = _code()
                serial = f'JIP-{_uid().upper()}'
                scanned = random.random() < 0.4
                scanner = random.choice(santeniklar) if scanned else None
                qr = QRCode.objects.create(
                    code=raw,
                    hash_code=hsh,
                    serial_number=serial,
                    points=batch.points_per_code,
                    store=batch.store,
                    batch=batch,
                    is_scanned=scanned,
                    scanned_by=scanner,
                    scanned_at=timezone.now() - timedelta(days=random.randint(0, 30)) if scanned else None,
                )
                qrcodes.append(qr)
                if scanned and scanner:
                    scanner.points += batch.points_per_code
                    scanner.save(update_fields=['points'])
        return qrcodes

    # ------------------------------------------------------------------
    def _create_seller_txns(self, sotuvchilar, stores):
        txn_types = ['manual_add', 'sales_bonus', 'correction']
        for seller in sotuvchilar:
            store = random.choice(stores)
            for _ in range(3):
                SellerPointsTransaction.objects.create(
                    seller=seller,
                    store=store,
                    transaction_type=random.choice(txn_types),
                    points=random.randint(50, 500),
                    sales_amount_usd=round(random.uniform(500, 5000), 2),
                    period_start=date.today().replace(day=1),
                    period_end=date.today(),
                    note='Test tranzaksiya',
                )

    # ------------------------------------------------------------------
    def _create_gifts(self):
        gifts_data = [
            ('Maxsus asboblar to\'plami', 'Набор специнструментов', 200),
            ('JIP futbolkasi', 'Футболка JIP', 100),
            ('Santexnik sumkasi', 'Сумка сантехника', 350),
            ('Termos (1L)', 'Термос 1л', 150),
            ('JIP kepkasi', 'Кепка JIP', 80),
        ]
        for name_uz, name_ru, cost in gifts_data:
            Gift.objects.get_or_create(
                name_uz_latin=name_uz,
                defaults={
                    'name_ru': name_ru,
                    'description_uz_latin': f'{name_uz} — JIP sovg\'asi',
                    'description_ru': f'{name_ru} — подарок JIP',
                    'image': 'gifts/placeholder.png',
                    'points_cost': cost,
                    'stock_quantity': random.randint(10, 100),
                    'is_active': True,
                    'order': cost // 100,
                },
            )

    # ------------------------------------------------------------------
    def _create_redemptions(self, santeniklar):
        gifts = list(Gift.objects.filter(is_active=True)[:3])
        if not gifts:
            return
        statuses = ['pending', 'approved', 'completed', 'rejected']
        for user in santeniklar[:5]:
            gift = random.choice(gifts)
            if user.points >= gift.points_cost:
                GiftRedemption.objects.get_or_create(
                    user=user,
                    gift=gift,
                    defaults={
                        'status': random.choice(statuses),
                        'admin_notes': 'Test ariza — seed_test_data',
                    },
                )
