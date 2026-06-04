"""Bir martalik tozalash: 1..811 oralig'idan tashqari skretch-kartalarni o'chirish.

Talab (2026-06-04, @Kobiljonovs): admin paneldagi skretch-kartalardan FAQAT
2-iyunda yaratilgan PROMO-00000001 .. PROMO-00000811 (global sequence_number 1..811)
qolsin, qolganlari o'chirilsin.

Nega migration?  Admin panel QRCode'ni o'chirishga ruxsat bermaydi (NoDelete),
management command esa deploy paytida avtomatik ishlamaydi. Data-migration `migrate`
bosqichida bir marta avtomatik bajariladi (Railway deploy) va qayta takrorlanmaydi.

QRCode'ga bog'liq yozuvlar CASCADE bilan birga o'chadi (MonthlyPromoTicket OneToOne,
QRCodeScanAttempt FK). Teskari yo'nalish: no-op (tiklab bo'lmaydi).
"""
from django.db import migrations, models

KEEP_FROM = 1
KEEP_TO = 811


def delete_extra_cards(apps, schema_editor):
    QRCode = apps.get_model('core', 'QRCode')
    qs = QRCode.objects.filter(
        ~models.Q(sequence_number__range=(KEEP_FROM, KEEP_TO))
        | models.Q(sequence_number__isnull=True)
    )
    deleted, _ = qs.delete()
    print(
        f"\n[0082] Skretch-karta tozalash: {deleted} qator o'chdi "
        f"(qoldi sequence_number {KEEP_FROM}..{KEEP_TO})."
    )


def noop_reverse(apps, schema_editor):
    # O'chirilgan kartalarni tiklab bo'lmaydi.
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0081_promotion_banner_fields'),
    ]

    operations = [
        migrations.RunPython(delete_extra_cards, noop_reverse),
    ]
