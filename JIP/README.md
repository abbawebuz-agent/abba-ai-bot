# JIP — Sodiqlik Dasturi

Santeniklar va sotuvchilar uchun Telegram bot + Web App + Django Admin platforma.

## Holat

| Faza | Holat |
|---|---|
| 1 — Setup (project skeleton, env, deploy config) | ✅ |
| 2 — Modellar + Admin (22 model, simple-history) | ✅ |
| 3 — Bot logikasi (aiogram FSM, QR scan, menus) | ✅ |
| 4 — Admin polish + Celery (batch ZIP generatsiya) | ✅ |
| 5 — Web App (santenik + sotuvchi mini app) | ✅ |
| 6 — Tarjimalar (uz_latin + ru) | ✅ |
| 7 — Testlar (22 unit test, admin smoke) | ✅ |

## Stack

- **Backend:** Python 3.11, Django 5.0, aiogram 3.5
- **DB:** PostgreSQL 15 (prod), SQLite (dev)
- **Cache + broker:** Redis 7
- **Task queue:** Celery 5.3 + beat
- **Bot:** aiogram 3.5 (webhook yoki polling)
- **Web App:** Telegram Mini App (vanilla JS, HTML, CSS)
- **Static files:** WhiteNoise (Railway/prod uchun)

## Loyiha tuzilmasi

```
JIP/
├── jip/                  Django project (settings, urls, celery, asgi/wsgi)
├── core/                 Models, admin, tasks, web app API
│   ├── models.py         22 ta model (TZ §5)
│   ├── admin.py          ModelAdmin'lar, batch generatsiya actions
│   ├── tasks.py          Celery tasks (batch ZIP, broadcast, snapshot)
│   ├── webapp_views.py   Telegram WebApp API endpoints
│   ├── webapp_auth.py    HMAC initData tekshiruv
│   ├── utils.py          QR generatsiya, hash, serial, ZIP
│   └── tests/            22 ta unit test
├── bot/                  aiogram bot
│   ├── bot.py            Dispatcher build
│   ├── handlers/         registration, promo, menu, language
│   ├── services.py       Async-wrapped DB operations
│   ├── translations.py   uz_latin + ru tarjima dict
│   ├── keyboards.py      Inline/reply keyboard'lar
│   └── webhook.py        Django webhook view
├── templates/
│   ├── webapp/           Telegram mini app HTML (santenik + seller)
│   └── admin/            Admin brending
├── locale/               .po fayllar (uz + ru)
└── requirements.txt
```

## Lokal ishga tushirish

```bash
# 1. Venv
python3 -m venv .venv
source .venv/bin/activate

# 2. Dependencies
pip install -r requirements.txt

# 3. .env
cp .env.example .env
# .env ni to'ldiring (eng kamida SECRET_KEY va TELEGRAM_BOT_TOKEN)

# 4. Migrate
python manage.py migrate
python manage.py createsuperuser

# 5. Run
python manage.py runserver
# Boshqa terminalda — bot:
python manage.py run_bot
# Yana boshqasida — celery:
celery -A jip worker -l info
celery -A jip beat -l info
```

Tekshirish:
- `http://localhost:8000/` — service info
- `http://localhost:8000/health/` — `{"status": "ok"}`
- `http://localhost:8000/admin/` — admin panel

## Test ishga tushirish

```bash
python manage.py test core.tests
# Natija: 22 tests, all green
```

## Railway deploy

1. Railway'da yangi loyiha
2. PostgreSQL va Redis plugin'larini qo'shing
3. GitHub repo'ni ulang
4. Variables:
   - `SECRET_KEY=<kuchli random>`
   - `DEBUG=False`
   - `DJANGO_SETTINGS_MODULE=jip.settings.production`
   - `ALLOWED_HOSTS=*.railway.app`
   - `TELEGRAM_BOT_TOKEN=<token>`
   - `TELEGRAM_WEBHOOK_URL=https://<domain>/bot/webhook/`
   - `TELEGRAM_WEBHOOK_SECRET=<random secret>`
   - `WEB_APP_URL=https://<domain>`
5. Deploy (Procfile + railway.json sozlangan)
6. Webhook'ni o'rnatish:
   ```bash
   python manage.py set_webhook
   ```

## Faza tafsilotlari

### Faza 1 — Setup
Project skeleton, Django config (base/local/production), Celery, WhiteNoise, .env.example, Railway config (Procfile, railway.json, nixpacks.toml).

### Faza 2 — Modellar
22 ta model TZ §5 bo'yicha: UzRegion, UzDistrict, Store, TelegramUser, QRCodeBatch, QRCode, QRCodeScanAttempt, PromoCodeAttempt, SellerPointsTransaction, Gift, GiftRedemption, MonthlyPromoTicket, BroadcastMessage, RegionMessageLog, Promotion, PrivacyPolicy, AdminContactSettings, VideoInstruction, LiveStream, LiveStreamWinner, MonthlyReminderSettings, MonthlyReminderLog. Initial migration generated.

### Faza 3 — Bot
aiogram 3 FSM bilan registration (til, ism, rol, privacy, telefon, lokatsiya, do'kon tasdiqlash sotuvchi uchun). QR scan handler (har matnli xabar promo kod sifatida tekshiriladi). Til o'zgartirish callback. Webhook view + polling management command.

### Faza 4 — Admin polish + Celery
- Batch yaratilganda avtomatik `generate_batch_zip` task ishga tushadi
- Sotuvchiga ball qo'shilganda `recalc_user_points` chaqiriladi
- Admin actions: Generate ZIP, Mark shipped/delivered
- JIP brending (ko'k rang, sayt nomi)

### Faza 5 — Web App
- Santenik mini app: balans, sovg'alar, buyurtmalar, top, promo kod kiritish
- Sotuvchi mini app: dashboard (kartalar statistikasi), tranzaksiyalar, batch'lar
- HMAC initData tekshiruv (xavfsizlik)
- 15+ REST endpoint

### Faza 6 — Tarjimalar
`bot/translations.py` — dict orqali, har element ikkala tilda. `locale/uz` va `locale/ru` .po fayllar admin model uchun.

### Faza 7 — Testlar
22 unit test: anti-fraud bloklash, balans hisob-kitobi (santenik va sotuvchi), QR scan (success/used/invalid/wrong_role/blocked/3-attempts-block), HMAC verify, utility functions. Admin smoke testlar (23 admin URL = 200 OK).

## Kerakli keyingi qadamlar (prod uchun)

- [ ] PostgreSQL bilan to'liq integratsion test
- [ ] Real Telegram bot bilan staging test
- [ ] OSM viloyat polygon'lari (`osm-data/uz-boundaries.geojson`) qo'shish
- [ ] `seed_districts.py` management command — barcha viloyat/tuman ma'lumotlarini yuklash
- [ ] CI workflow (lint + test)
- [ ] Backup script'lari (`scripts/backup_postgres.sh`)
- [ ] Sentry DSN va prod logging
- [ ] Anti-fraud dashboard (admin'da shubhali harakatlar)
