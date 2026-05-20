# JIP — Sodiqlik Dasturi

Santeniklar va sotuvchilar uchun Telegram bot + Web App + Django Admin platforma.

## Stack
- Python 3.11+, Django 5
- aiogram 3 (Telegram bot)
- PostgreSQL 15, Redis 7
- Celery 5

## Lokal ishga tushirish

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
# .env ni to'ldiring (DATABASE_URL, REDIS_URL, TELEGRAM_BOT_TOKEN)

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Railway deploy

1. Yangi Railway loyiha yarating
2. **PostgreSQL** va **Redis** plagin'larini qo'shing
3. GitHub repo'ni ulang
4. Environment variables qo'shing (`.env.example` dan ko'chiring):
   - `SECRET_KEY` (kuchli random string)
   - `DEBUG=False`
   - `ALLOWED_HOSTS=*.railway.app,<sizning domeningiz>`
   - `DJANGO_SETTINGS_MODULE=jip.settings.production`
   - `TELEGRAM_BOT_TOKEN`
   - `WEB_APP_URL=https://<sizning-domeningiz>.railway.app`
   - `DATABASE_URL` — Railway avtomatik beradi (Postgres plugin)
   - `REDIS_URL` — Railway avtomatik beradi (Redis plugin)
5. Deploy bosing

Railway `Procfile` ni avtomatik o'qiydi:
- `release: python manage.py migrate` (deploy oldidan)
- `web: gunicorn jip.wsgi:application` (asosiy server)

## Holat

Faza 1 (Setup) tugallandi. Keyingi fazalar:
- Faza 2 — Modellar (Store, QRCodeBatch, TelegramUser, QRCode, ...)
- Faza 3 — Bot logikasi (registration, QR scan)
- Faza 4 — Admin panel
- Faza 5 — Web App
- Faza 6 — Tarjimalar
- Faza 7 — Testlar
