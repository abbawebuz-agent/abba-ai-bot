"""Allaqachon ro'yxatdan o'tib bo'lgan santexniklarga +30 ball xush kelibsiz bonini
beradi (bir martagina). Ball qiymati settings.WELCOME_BONUS_POINTS (default 30).

Faqat flag o'rnatiladi — haqiqiy +30 ball calculate_points() orqali avtomatik
qo'shiladi (welcome_bonus_awarded=True bo'lsa total_earned ga qo'shiladi). Shu sabab
bu yerda points maydonini qo'lda o'zgartirmaymiz (ikki marta hisoblanmasligi uchun)."""
from django.conf import settings
from django.db import migrations


def award_existing(apps, schema_editor):
    TelegramUser = apps.get_model('core', 'TelegramUser')
    bonus = getattr(settings, 'WELCOME_BONUS_POINTS', 30)
    if bonus <= 0:
        return
    # Ro'yxati tugagan santexniklar: til + maxfiylik + telefon + viloyat
    qs = (
        TelegramUser.objects
        .filter(user_type='santenik', welcome_bonus_awarded=False, privacy_accepted=True, region__isnull=False)
        .exclude(phone_number__isnull=True)
        .exclude(phone_number='')
        .exclude(language__isnull=True)
        .exclude(language='')
    )
    qs.update(welcome_bonus_awarded=True)


def reverse(apps, schema_editor):
    # Qaytarish: faqat shu migratsiya bergan bonini olib tashlash imkoni yo'q
    # (keyin yangi ro'yxatdan o'tganlar bilan aralashib ketadi), shuning uchun no-op.
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0085_telegramuser_welcome_bonus_awarded'),
    ]

    operations = [
        migrations.RunPython(award_existing, reverse),
    ]
