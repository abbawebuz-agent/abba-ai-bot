"""Loyihani real ishga tushirishdan oldin BARCHA test ma'lumotlarini tozalash.

To'liq clean slate: hamma TelegramUser (santexnik + sotuvchi), QRCode/promokod,
partiyalar, do'konlar, sovg'a so'rovlari, ball tranzaksiyalari, oylik biletlar,
promokod urinishlari, Seller'lar va ularning batch'lari o'chiriladi.

SAQLANADI (config / katalog):
    - UzRegion, UzDistrict (viloyat/tuman)
    - Gift (sovg'alar katalogi — faqat so'rovlar/redemption o'chadi)
    - Promotion (bannerlar), PrivacyPolicy, AdminContactSettings
    - VideoInstruction, MonthlyReminderSettings, BroadcastMessage shablonlari
    - LiveStream (g'oliblar tozalanadi, oqimning o'zi qoladi)
    - auth.User (Django admin loginlari) — hech qachon tegilmaydi
    - SellerRegistrationCode — o'chmaydi, faqat "ishlatilgan" holati reset bo'ladi

Standart holatda DRY-RUN: nima o'chishini sanab ko'rsatadi, lekin o'chirmaydi.
Haqiqatan o'chirish uchun:  python manage.py reset_for_launch --confirm
"""
from django.core.management.base import BaseCommand
from django.db import transaction

from core.models import (
    TelegramUser, QRCode, QRCodeBatch, Store,
    MonthlyPromoTicket, QRCodeScanAttempt, PromoCodeAttempt,
    GiftRedemption, SellerPointsTransaction, LiveStreamWinner,
    Seller, SellerBatch, SellerRegistrationCode,
    RegionMessageLog, ActivityLog,
)

# O'chirish tartibi MUHIM — PROTECT bog'lanishlar sababli "bola"lar avval.
#   QRCode.store/batch -> PROTECT      => QRCode avval, keyin batch/store
#   MonthlyPromoTicket.store -> PROTECT => ticket avval, keyin store
#   SellerPointsTransaction.seller -> PROTECT (TelegramUser)
#   LiveStreamWinner.user -> PROTECT (TelegramUser)
#   Store.owner -> PROTECT (TelegramUser) => store avval, keyin user
DELETE_ORDER = [
    ('Oylik biletlar (MonthlyPromoTicket)', MonthlyPromoTicket),
    ('QR skan urinishlari (QRCodeScanAttempt)', QRCodeScanAttempt),
    ('Promokod urinishlari (PromoCodeAttempt)', PromoCodeAttempt),
    ("Sovg'a so'rovlari (GiftRedemption)", GiftRedemption),
    ('Sotuvchi ball tranzaksiyalari (SellerPointsTransaction)', SellerPointsTransaction),
    ("Jonli efir g'oliblari (LiveStreamWinner)", LiveStreamWinner),
    ('Promokodlar / QR-kartalar (QRCode)', QRCode),
    ('Sotuvchi partiyalari (SellerBatch)', SellerBatch),
    ('QR partiyalari (QRCodeBatch)', QRCodeBatch),
    ("Do'konlar (Store)", Store),
    ('Sotuvchilar — yangi struktura (Seller)', Seller),
    ('Region xabar loglari (RegionMessageLog)', RegionMessageLog),
    ('Faollik loglari (ActivityLog)', ActivityLog),
    ('Foydalanuvchilar (TelegramUser)', TelegramUser),
]


class Command(BaseCommand):
    help = "Real start oldidan BARCHA test ma'lumotlarini tozalaydi (config/katalog saqlanadi)."

    def add_arguments(self, parser):
        parser.add_argument(
            '--confirm', action='store_true',
            help="Haqiqatan o'chirish. Bo'lmasa faqat dry-run (sanab ko'rsatadi).",
        )

    def handle(self, *args, **options):
        confirm = options['confirm']

        self.stdout.write(self.style.MIGRATE_HEADING(
            '\n=== JIP: real start uchun ma\'lumotlarni tozalash ==='
        ))
        self.stdout.write('Rejim: ' + (
            self.style.ERROR('HAQIQIY O\'CHIRISH (--confirm)') if confirm
            else self.style.WARNING('DRY-RUN (hech narsa o\'chmaydi)')
        ))

        # Avval hozirgi sonlarni ko'rsatamiz
        self.stdout.write('\nO\'chiriladigan yozuvlar:')
        total = 0
        for label, model in DELETE_ORDER:
            cnt = model.objects.count()
            total += cnt
            self.stdout.write(f'  - {label}: {self.style.NOTICE(str(cnt))}')

        used_codes = SellerRegistrationCode.objects.filter(is_used=True).count()
        self.stdout.write(
            f'\nReset qilinadi (o\'chmaydi): SellerRegistrationCode "ishlatilgan" -> '
            f'{self.style.NOTICE(str(used_codes))} ta bo\'shatiladi'
        )

        # Saqlanadigan katalogni ko'rsatamiz (ishonch uchun)
        from core.models import Gift, UzRegion, Promotion
        self.stdout.write(self.style.SUCCESS(
            f'\nSAQLANADI: Gift={Gift.objects.count()}, '
            f'UzRegion={UzRegion.objects.count()}, '
            f'Promotion(banner)={Promotion.objects.count()}, '
            f'Django admin loginlari — tegilmaydi.'
        ))

        if not confirm:
            self.stdout.write(self.style.WARNING(
                f'\n[DRY-RUN] Jami {total} ta yozuv o\'chiriladi. '
                f'Haqiqatan o\'chirish uchun:\n'
                f'    python manage.py reset_for_launch --confirm\n'
            ))
            return

        # --- HAQIQIY O'CHIRISH ---
        self.stdout.write(self.style.ERROR('\nO\'chirilmoqda...'))
        deleted_summary = []
        with transaction.atomic():
            for label, model in DELETE_ORDER:
                n, _ = model.objects.all().delete()
                deleted_summary.append((label, n))
                self.stdout.write(f'  ✓ {label}: {n} qator o\'chdi')

            # Registratsiya kodlarini qayta foydalanish uchun bo'shatamiz
            reset_n = SellerRegistrationCode.objects.filter(is_used=True).update(
                is_used=False, used_by=None, used_at=None,
            )
            self.stdout.write(f'  ✓ SellerRegistrationCode reset: {reset_n} ta bo\'shatildi')

        self.stdout.write(self.style.SUCCESS(
            '\n✅ Tozalash tugadi. Endi loyihaga real data qo\'shsa bo\'ladi.\n'
            'Tekshirish: TelegramUser=%d, QRCode=%d, Store=%d' % (
                TelegramUser.objects.count(),
                QRCode.objects.count(),
                Store.objects.count(),
            )
        ))
