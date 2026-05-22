"""
Сид тестовых данных для WebApp под telegram_id=390736292.
Запуск: docker-compose exec web python /app/seed_test_data.py
Идемпотентен — повторный запуск не плодит дубли.
"""
import os
import sys
import io
import base64
from datetime import timedelta, date, datetime, time as dtime

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mona.settings.local')
django.setup()

from django.core.files.base import ContentFile
from django.utils import timezone

from core.models import (
    TelegramUser, QRCode, MonthlyPromoTicket, Gift, GiftRedemption,
    Promotion, LiveStream, LiveStreamWinner,
)

TG_ID = 390736292

# Минимальная валидная PNG 1×1 transparent
PNG_1x1 = base64.b64decode(
    'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=='
)


def png_file(name):
    return ContentFile(PNG_1x1, name=name)


# ──────────────────────────────────────────────────────────
# 1. Пользователь
# ──────────────────────────────────────────────────────────
user, created = TelegramUser.objects.update_or_create(
    telegram_id=TG_ID,
    defaults={
        'username': 'test_user',
        'first_name': 'Test',
        'last_name': 'User',
        'phone_number': '+998901234567',
        'user_type': 'electrician',
        'points': 1240,
        'is_active': True,
        'language': 'ru',
        'privacy_accepted': True,
    },
)
print(f"User: {'created' if created else 'updated'} {user} (points={user.points})")


# ──────────────────────────────────────────────────────────
# 2. Promotions (баннеры)
# ──────────────────────────────────────────────────────────
promo_data = [
    ('Mega-aksiya: 2× ballar', date.today()),
    ('Yangi yil sovg‘alari', date.today() + timedelta(days=10)),
    ('Yozgi imtiyozlar', date.today() + timedelta(days=25)),
]
for i, (title, dt) in enumerate(promo_data):
    p, created = Promotion.objects.update_or_create(
        title=title,
        defaults={'date': dt, 'is_active': True, 'order': i},
    )
    if not p.image:
        p.image.save(f'promo_{i}.png', png_file(f'promo_{i}.png'), save=True)
    print(f"Promotion: {'created' if created else 'updated'} #{p.id} {title}")


# ──────────────────────────────────────────────────────────
# 3. Gifts (каталог)
# ──────────────────────────────────────────────────────────
gifts_data = [
    ('Otvyortka to‘plami', 'Набор отверток',     400,  None,         0),
    ('Multimetr DT-832',   'Мультиметр DT-832',  900,  'electrician', 1),
    ('Drel akkumulyatorli','Дрель аккумуляторная', 1200, None,         2),
    ('Kabel sumkasi',      'Сумка для кабеля',   1500, None,         3),
    ('Kalit naborlari',    'Набор ключей',       2200, 'electrician', 4),
    ('Lazer rulet',        'Лазерный дальномер', 3200, None,         5),
]
for nm_uz, nm_ru, cost, utype, order in gifts_data:
    g, created = Gift.objects.update_or_create(
        name_uz_latin=nm_uz,
        defaults={
            'name_ru': nm_ru,
            'description_uz_latin': f'{nm_uz} — sifatli sovg‘a, ish uchun ideal.',
            'description_ru': f'{nm_ru} — качественный подарок, идеально для работы.',
            'points_cost': cost,
            'user_type': utype,
            'is_active': True,
            'order': order,
        },
    )
    if not g.image:
        g.image.save(f'gift_{order}.png', png_file(f'gift_{order}.png'), save=True)
    print(f"Gift: {'created' if created else 'updated'} #{g.id} {nm_uz} ({cost} ball)")


# ──────────────────────────────────────────────────────────
# 4. QR-коды и билеты розыгрыша
#    — 5 в текущем месяце (с MonthlyPromoTicket → ticket_number)
#    — 3 в прошлом месяце (архив)
# ──────────────────────────────────────────────────────────
now = timezone.now()
this_month_start = date(now.year, now.month, 1)
prev_month_anchor = (this_month_start - timedelta(days=1))
prev_month_start = date(prev_month_anchor.year, prev_month_anchor.month, 1)


def make_qr(idx, scanned_at_aware, with_ticket: bool, points=50):
    code_type = 'electrician'
    code = f"E{str(scanned_at_aware.month).zfill(2)}{str(scanned_at_aware.day).zfill(2)}{idx:03d}"
    qr, was_created = QRCode.objects.get_or_create(
        code=code,
        defaults={
            'code_type': code_type,
            'hash_code': f"H{code[-6:]}",
            'serial_number': f"E{scanned_at_aware.year}{scanned_at_aware.month:02d}{idx:04d}",
            'points': points,
        },
    )
    if not qr.is_scanned:
        qr.is_scanned = True
        qr.scanned_at = scanned_at_aware
        qr.scanned_by = user
        qr.save(update_fields=['is_scanned', 'scanned_at', 'scanned_by'])
    if with_ticket:
        month_first = date(scanned_at_aware.year, scanned_at_aware.month, 1)
        # подбираем следующий свободный order в (month, user_type)
        existing_for_qr = MonthlyPromoTicket.objects.filter(qr_code=qr).first()
        if existing_for_qr is None:
            last_order = MonthlyPromoTicket.objects.filter(
                month=month_first, user_type=code_type
            ).order_by('-order').values_list('order', flat=True).first() or 0
            MonthlyPromoTicket.objects.create(
                month=month_first,
                qr_code=qr,
                user=user,
                user_type=code_type,
                order=last_order + 1,
                scanned_at=scanned_at_aware,
            )
    return qr


# Текущий месяц — 5 билетов
for i in range(1, 6):
    day = min(now.day, 28) - (i - 1)
    if day < 1:
        day = i
    scanned_at = timezone.make_aware(
        datetime.combine(date(now.year, now.month, day), dtime(10 + i, 30))
    )
    make_qr(i, scanned_at, with_ticket=True, points=50 if i % 2 else 100)

# Прошлый месяц — 3 архивные карточки (без билета или с билетом-архивом)
for i in range(1, 4):
    scanned_at = timezone.make_aware(
        datetime.combine(date(prev_month_start.year, prev_month_start.month, 5 + i), dtime(12, 0))
    )
    make_qr(50 + i, scanned_at, with_ticket=True, points=50)

print(f"QR-коды для пользователя: {QRCode.objects.filter(scanned_by=user).count()}")
print(f"Билеты в этом месяце: {MonthlyPromoTicket.objects.filter(user=user, month=this_month_start).count()}")


# ──────────────────────────────────────────────────────────
# 5. Активный заказ (GiftRedemption)
# ──────────────────────────────────────────────────────────
gift_for_order = Gift.objects.filter(is_active=True).order_by('points_cost').first()
if gift_for_order:
    redemption, created = GiftRedemption.objects.get_or_create(
        user=user,
        gift=gift_for_order,
        status='approved',
        defaults={'admin_notes': 'Test order'},
    )
    print(f"Redemption: {'created' if created else 'updated'} #{redemption.id} status={redemption.status}")


# ──────────────────────────────────────────────────────────
# 6. Прямые эфиры (1 предстоящий + 1 прошедший с победителями)
# ──────────────────────────────────────────────────────────
upcoming, created = LiveStream.objects.update_or_create(
    title_uz_latin='Aprel oyi tirik efiri',
    defaults={
        'title_ru': 'Прямой эфир — апрель',
        'description_uz_latin': 'Bu oydagi g‘oliblar e‘lon qilinadi.',
        'description_ru': 'Объявим победителей этого месяца.',
        'scheduled_at': timezone.now() + timedelta(days=3),
        'stream_url': 'https://t.me/test_channel/1',
        'is_active': True,
    },
)
if not upcoming.cover:
    upcoming.cover.save('live_upcoming.png', png_file('live_upcoming.png'), save=True)
print(f"Upcoming live: {'created' if created else 'updated'} #{upcoming.id}")

past, created = LiveStream.objects.update_or_create(
    title_uz_latin='Mart oyi g‘oliblari',
    defaults={
        'title_ru': 'Победители марта',
        'description_uz_latin': 'O‘tgan oyning g‘oliblari ro‘yxati.',
        'description_ru': 'Список победителей прошлого месяца.',
        'scheduled_at': timezone.now() - timedelta(days=14),
        'stream_url': 'https://t.me/test_channel/0',
        'is_active': True,
    },
)
if not past.cover:
    past.cover.save('live_past.png', png_file('live_past.png'), save=True)
print(f"Past live: {'created' if created else 'updated'} #{past.id}")

# Победители для прошедшего эфира — нужны другие пользователи (тип electrician/seller)
def ensure_user(tid, fname, utype):
    u, _ = TelegramUser.objects.update_or_create(
        telegram_id=tid,
        defaults={
            'first_name': fname,
            'phone_number': f'+99890000{tid % 10000}',
            'user_type': utype,
            'points': 500,
            'is_active': True,
            'language': 'uz_latin',
            'privacy_accepted': True,
        },
    )
    return u

winners_data = [
    # (telegram_id, first_name, user_type, position, prize_uz, prize_ru)
    (1000001, 'Akbar Toshmatov',    'electrician', 1, 'Drel akkumulyatorli', 'Дрель аккумуляторная'),
    (1000002, 'Sardor Karimov',     'electrician', 2, 'Multimetr DT-832',    'Мультиметр DT-832'),
    (1000003, 'Bobur Yusupov',      'electrician', 3, 'Otvyortka to‘plami',  'Набор отверток'),
    (1000004, 'Dilshod Rakhimov',   'electrician', 4, 'Kabel sumkasi',       'Сумка для кабеля'),
    (1000005, 'Aziz Saidov',        'seller',      1, 'Lazer rulet',         'Лазерный дальномер'),
    (1000006, 'Nodir Tursunov',     'seller',      2, 'Kalit naborlari',     'Набор ключей'),
    (1000007, 'Jahongir Nasirov',   'seller',      3, 'Multimetr DT-832',    'Мультиметр DT-832'),
]

for tid, fname, utype, pos, pr_uz, pr_ru in winners_data:
    wu = ensure_user(tid, fname, utype)
    LiveStreamWinner.objects.update_or_create(
        live_stream=past,
        user=wu,
        defaults={
            'position': pos,
            'prize_text_uz_latin': pr_uz,
            'prize_text_ru': pr_ru,
        },
    )

print(f"Winners for past stream: {past.winners.count()}")
print('\n✅ Сид завершён. Открой WebApp:')
print(f'   https://securities-leonard-displays-charged.trycloudflare.com/api/webapp/?telegram_id={TG_ID}')
