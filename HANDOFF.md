# JIP Loyalty Platform — HANDOFF (loyiha topshirish hujjati)

> **Maqsad:** Bu hujjat JIP loyihasini boshqa Claude agentiga (yoki dasturchiga) to'liq topshirish uchun. Hech narsani oldindan bilmagan holatda ham loyihani davom ettira olish uchun yetarli.
> **Sana:** 2026-06-04
> **Repo path:** `/Users/a1111/mona/`

---

## 1. Loyiha nima qiladi?

**JIP** — santexnika mahsulotlari uchun **loyalty (sodiqlik) dasturi**. Telegram bot + Web App + admin panel.

**2 ta foydalanuvchi roli:**

1. **Santexnik** (`user_type='santenik'`) — mahsulot qadog'idagi **skretch-karta / promokod** ni kiritadi → ball oladi → to'plagan balliga **sovg'a** so'raydi.
2. **Sotuvchi** (`user_type='sotuvchi'`) — do'kon egasi. Admin uning sotuvlari bo'yicha partiya yaratadi → ballar avtomatik hisoblanadi.

> "Do'kon" (Store) roli **alohida bot roli sifatida olib tashlangan** — endi Store faqat ma'muriy model (QR partiyalarini guruhlash uchun).

---

## 2. Kirish / Accesslar (CREDENTIALS)

| Nima | Qiymat |
|------|--------|
| **Production** | https://jip-production.up.railway.app/ |
| **Admin panel** | https://jip-production.up.railway.app/admin/ — login: `admin` / parol: `123` |
| **Yangi admin SPA** | https://jip-production.up.railway.app/jip-admin/ |
| **Telegram bot** | `@santexnik_JIP_bot` |
| **GitHub repo** | https://github.com/abbawebuz-agent/abba-ai-bot.git (⚠️ nomi "abba" lekin ichida JIP kodi) |
| **Deploy branch** | `deploy` → push qilinganda Railway avtomatik deploy qiladi (~2 daqiqa) |
| **Hosting** | Railway (Docker, `Dockerfile.prod`) |
| **DB** | PostgreSQL 18.4 (Railway managed) |
| **DB Backup kanali** | Telegram: `JIP Loyalty Back UP` (chat_id: `-1003859633634`) — har kuni 04:00 (Asia/Tashkent) |

⚠️ **Maxfiy kalitlar** (SECRET_KEY, TELEGRAM_BOT_TOKEN, DATABASE_URL, CLOUDINARY_URL, SENTRY_DSN va h.k.) **Railway environment variables** ichida. Lokal `.env` yo'q. Strukturasi `.env.example` da ko'rsatilgan.

---

## 3. Texnologik stack

- **Backend:** Django 5.0.1 + Django REST Framework
- **Bot:** aiogram 3.3 (FSM states bilan), webhook rejimida
- **Frontend (webapp):** React 18 + Babel standalone (CDN, build step YO'Q — to'g'ridan-to'g'ri `<script type="text/babel">`)
- **Frontend (yangi admin SPA):** React + Babel, `scripts/build_admin_spa.js` bilan `bundle.js` ga yig'iladi
- **Admin:** django-jazzmin 2.6 + custom CSS (`jip_theme_2026.css`)
- **DB:** PostgreSQL (+ `django-simple-history` audit uchun)
- **Queue:** Celery 5.3 + Redis (region broadcast, backup, eslatmalar)
- **Server:** uvicorn (ASGI) — `mona.asgi:application`
- **Media:** Cloudinary (Railway efemer FS sababli) — `CLOUDINARY_URL` env bo'lganda faollashadi
- **Monitoring:** Sentry

---

## 4. Repo tuzilishi (asosiy qismlar)

```
mona/
├── manage.py
├── railway.json              ⚠️ DEPLOY START COMMAND shu yerda (pastga qarang!)
├── Dockerfile.prod           # Railway build
├── requirements.txt
├── .env.example              # Kerakli env o'zgaruvchilar ro'yxati
│
├── mona/                     # Django project
│   ├── settings/
│   │   ├── base.py           # Umumiy sozlamalar
│   │   ├── local.py          # Lokal dev
│   │   └── production.py     # Production (Railway shuni ishlatadi)
│   ├── asgi.py               # uvicorn entry point
│   └── celery.py
│
├── core/                     # ASOSIY Django app
│   ├── models.py             ⭐ 27 ta model — butun data modeli shu yerda
│   ├── admin.py              # Jazzmin admin (barcha model adminlari)
│   ├── webapp_views.py       # Santexnik webapp API endpointlari
│   ├── views_jip_admin.py    # Yangi admin SPA backend (/jip-admin/)
│   ├── api/                  # DRF API (serializers, views, urls)
│   ├── urls.py
│   ├── tasks.py              # Celery tasklar (backup, broadcast, remind)
│   ├── signals.py
│   ├── monthly_promo.py      # Oylik promo bilet logikasi
│   ├── messaging.py          # Bot xabar yuborish helperlari
│   ├── regions.py / uz_districts_data.py / boundary_lookup.py  # Viloyat/tuman geo
│   ├── static/
│   │   ├── webapp/           # Santexnik webapp statiklari
│   │   └── admin_ui/spa/     # Yangi admin SPA (app.jsx, pages-*.jsx, bundle.js)
│   └── management/commands/  # ⭐ Management buyruqlari (pastga qarang)
│
├── bot/                      # Telegram bot
│   ├── bot.py                ⭐ Barcha handlerlar + FSM (eng katta fayl)
│   ├── translations.py       ⚠️ Barcha bot matnlari (UZ/RU) — APOSTROF ehtiyot!
│   ├── webhook.py
│   ├── location_picker.py
│   └── management/commands/run_bot.py
│
├── templates/
│   ├── webapp/
│   │   ├── index.html        # Santexnik SPA (joriy)
│   │   ├── index_v5.html     # Santexnik webapp v5 (yangi dizayn)
│   │   └── seller.html       # Sotuvchi webapp
│   ├── admin/                # Jazzmin override'lar
│   └── jip_admin/            # Yangi admin SPA shell
│
├── frontend/                 # Alohida React frontend (npm build) — admin_ui uchun
├── scripts/                  # Deploy/backup yordamchi skriptlar
│   ├── build_admin_spa.js    # Admin SPA bundle yig'ish
│   ├── backup_postgres.sh / restore_postgres.sh
│   └── setup_ngrok.sh        # Lokal webapp test uchun
├── locale/                   # i18n (uz, ru)
└── documentations/           # Qo'shimcha hujjatlar
```

**Fayl statistikasi:** ~72 Python fayl (core+bot+mona), 84 migration, ~6100 JS/JSX (asosan frontend/admin SPA).

---

## 5. Data modeli (`core/models.py` — 27 model)

**Asosiy (transaksion):**
- `TelegramUser` — santexnik/sotuvchi. `telegram_id`, `user_type`, `points`, `region`, `language`, `privacy_accepted`, promo bloklash maydonlari
- `QRCode` — **= promokod / skretch-karta**. `code`, `hash_code`, `serial_number`, `points`, `store`, `batch`, `scanned_by`
- `QRCodeBatch` — QR partiyasi (do'konga biriktirilgan)
- `Store` — do'kon (owner = sotuvchi)
- `MonthlyPromoTicket` — oylik o'yin bileti (har skanlangan QR = 1 bilet)
- `GiftRedemption` — sovg'a so'rovi (4 bosqich: pending→approved→completed/rejected)
- `SellerPointsTransaction` — sotuvchi ball tranzaksiyasi
- `QRCodeScanAttempt`, `PromoCodeAttempt` — urinish loglari (firibgarlikka qarshi)
- `Seller`, `SellerBatch` — yangi sotuvchi strukturasi
- `LiveStream`, `LiveStreamWinner` — jonli efir o'yinlari

**Config / katalog (saqlanadigan):**
- `UzRegion`, `UzDistrict` — viloyat/tuman
- `Gift` — sovg'alar katalogi
- `Promotion` — webapp banner slider
- `PrivacyPolicy`, `AdminContactSettings`, `VideoInstruction`
- `MonthlyReminderSettings`, `MonthlyReminderLog`
- `SellerRegistrationCode` — sotuvchi ro'yxatdan o'tish 8-raqamli ID
- `BroadcastMessage`, `RegionMessageLog` — ommaviy xabar
- `ClaudeInbox` — bot @mention'larni saqlash
- `ActivityLog` — faollik logi

> ⚠️ **PROTECT bog'lanishlar** (o'chirishda muhim): `Store.owner→User`, `QRCode.store/batch→Store/Batch`, `MonthlyPromoTicket.store→Store`, `SellerPointsTransaction.seller→User`, `LiveStreamWinner.user→User`. Qolganlari CASCADE/SET_NULL.

---

## 6. Bot ro'yxatdan o'tish oqimi (`bot/bot.py`)

**Santexnik:**
`/start` → til tanlash → maxfiylik siyosati → telefon (+998 shablon) → 4 raqamli SMS kod (Telegram Gateway `@VerificationCodes`, 1 daqiqa cooldown) → GPS joylashuv → viloyat tanlash (inline) → bosh menyu + promokod so'rash

**Sotuvchi:**
`/start` → til → ism → "Men sotuvchiman" → 8 raqamli ID (`SellerRegistrationCode`) → video → privacy → telefon → joylashuv → muvaffaqiyat + WebApp tugma

**FSM States (`RegistrationStates`):** `waiting_for_language`, `waiting_for_privacy`, `waiting_for_phone`, `waiting_for_verification_code`, `waiting_for_location`, `waiting_for_region`, `waiting_for_promo_code`

**`is_registration_complete`** = `language AND privacy_accepted AND phone_number AND region_id`

---

## 7. Webapp

**Santexnik (5 tab):** 🏠 Bosh sahifa (hero karta, banner slider, promokod input, top-5) / 🎁 Sovg'alar / 📋 Promo tarix / 📦 Buyurtmalar (4 bosqichli progress) / 👤 Profil

**Sotuvchi (5 tab):** Главная → Баллы → Партии → Топ → Расчёт

**Asosiy API (`core/webapp_views.py`):**
```
/api/webapp/user/?telegram_id=X
/api/webapp/gifts/?telegram_id=X
/api/webapp/gifts/<id>/request/
/api/webapp/qr-history/?telegram_id=X
/api/webapp/redemptions/?telegram_id=X
/api/webapp/top-users/
/api/webapp/promo-history/?telegram_id=X
/api/webapp/admin-contact/
/api/webapp/translations/?lang=uz_latin
/api/webapp/seller/
```

---

## 8. Deployment ⚠️ MUHIM

Railway `Dockerfile.prod` bilan build qiladi va **`railway.json` dagi `startCommand`** ni ishga tushiradi:

```
migrate --noinput
  → collectstatic --noinput --clear
  → createsuperuser --no-input   (admin/123)
  → seed_test_data               ⚠️⚠️⚠️ HAR DEPLOYДА TEST DATA YARATADI!
  → set_webhook
  → uvicorn mona.asgi:application
```

### 🔴 ENG MUHIM OGOHLANTIRISH (real start uchun):
`startCommand` (va `Dockerfile.prod` ning `CMD` qatori) **har deployда `seed_test_data` ni chaqiradi**. Demak bazani test datadan tozalasak ham, **keyingi deployда test santexnik/sotuvchi/do'kon/QR'lar QAYTA yaratiladi.**

**Real ishga tushirishdan oldin SHART:** `railway.json` va `Dockerfile.prod` dan `(python manage.py seed_test_data 2>/dev/null || true) &&` qismini **olib tashlash**. Aks holda tozalash behuda.

Deploy qilish:
```bash
git add . && git commit -m "..." && git push origin deploy
# Railway avtomatik deploy (~2 daqiqa)
```

---

## 9. Management buyruqlari (`core/management/commands/`)

| Buyruq | Vazifa |
|--------|--------|
| `seed_test_data [--flush]` | Test data yaratadi (⚠️ har deployда ishlaydi). `--flush` faqat `testuser*`/`[TEST]` larni o'chiradi |
| **`reset_for_launch [--confirm]`** | ⭐ **YANGI (biz qo'shdik)** — real start oldidan BARCHA test datani tozalaydi. Default dry-run, `--confirm` bilan o'chiradi. Config/katalog saqlanadi |
| `backup_db` | Bazani Telegram kanalga backup qiladi |
| `restore_db` | Backupdan tiklaydi |
| `set_webhook [--delete]` | Telegram webhook o'rnatadi |
| `import_telegram_users`, `import_smartup_ids` | Import skriptlari |
| `backfill_monthly_promo_tickets` | Eski QR'lar uchun bilet yaratadi |
| `send_broadcast`, `send_message`, `remind_registration` | Xabar yuborish |
| `push_main_menu_keyboard`, `request_user_location` | Bot keyboard/lokatsiya |
| `run_bot` (bot/management) | Botni polling rejimida ishga tushiradi |

---

## 10. Nimalar QILINDI (git tarixidan)

So'nggi ishlar (yangidan eskiga):
- ✅ **`reset_for_launch`** command — real start oldidan test data tozalash (eng oxirgi, biz qo'shdik)
- ✅ **Banner slider** — admin boshqaradigan webapp banner (`Promotion` modeli)
- ✅ **Sovg'a rasmlari** — real mahsulot rasmlari, premium qora fon, `image_url` maydoni (internet havola)
- ✅ **Verification kod** — Telegram Gateway (`@VerificationCodes`) orqali SMS tasdiqlash
- ✅ **Cloudinary** — Railway efemer FS uchun doimiy media saqlash
- ✅ **Webapp v5** — santexnik uchun yangi to'liq dizayn (profil, maxfiylik, tarix, sovg'a kartalari)
- ✅ **JIP GROUP logo** — shaffof PNG, Telegram header rang+expand
- ✅ **Sotuvchi webapp** URL route tiklandi, `promo_from` auto-hisoblash
- ✅ **Region broadcast** — Celery fallback bilan
- ✅ **Claude Inbox** — bot @mention'larni saqlash + admin viewer
- ✅ **Admin buglar** — `BUGS_FOUND.md` da 20+ bug Puppeteer test bilan tuzatildi
- ✅ **Yangi admin SPA** (`/jip-admin/`) — React, 35 sahifa, bundle.js

---

## 11. Nima ISHLADI ✅

- Bot ro'yxatdan o'tish oqimi (santexnik + sotuvchi) — to'liq ishlaydi
- Promokod/QR skan → ball berish
- Sovg'a so'rash → admin tasdiqlash (4 bosqich)
- Webapp v5 dizayni
- Telegram Gateway SMS tasdiqlash
- Cloudinary media (Railway FS muammosini hal qildi)
- Avtomatik kunlik DB backup → Telegram kanal
- Jazzmin admin + yangi admin SPA
- Railway auto-deploy pipeline

---

## 12. Nima ISHLAMADI / qiyinchiliklar 🔴 (`BUGS_FOUND.md`)

**Tuzatilgan kritik buglar:**
- Batch yaratish 500 → migration 0072 + try/except (BUG-001)
- Gift qo'shish 500 → fieldsets tuzatildi (BUG-002)
- Sotuvchi ID qo'shish 403 → `/generate/` tugmasi orqali (BUG-003)
- Stores tab QR data → `scanned_by__user_type` filter (BUG-005)
- Media productionda yo'qoladi → Cloudinary (b9f081b), xlsx on-demand serve (27ba...)
- `core_historicalqrcode` sequence_number column yo'q → migration (b41b860)

**Qolgan (sekundar) muammolar:**
- BUG-012/021 — Sana formati aralash ("23 Май", "Май 21")
- BUG-013 — admin status badge'lari hardcoded RU
- BUG-015 — User detail sahifa tili (get_language conditional kerak)
- BUG-022 — Sidebar "Изменить пароль"/"Выйти" RU (Jazzmin internal)

**Takrorlanuvchi tuzoqlar (GOTCHAS):**
1. ⚠️ **`translations.py` da egri apostrof** (`'` U+2018/U+2019) → Django startup CRASH. Faqat to'g'ri `'` ishlatish!
2. ⚠️ **`seed_test_data` har deployда ishlaydi** (8-bo'lim) — real start oldidan o'chirish shart
3. ⚠️ **Gift modelда `user_type` yo'q** — `webapp_views.py` da filter qilmang
4. ⚠️ **JSX `style={{}}` Django template bilan to'qnashadi** → `{% verbatim %}` bilan o'rash
5. ⚠️ **postgresql-client-18** kerak (Dockerfile.prod) — backup uchun
6. ⚠️ **Railway efemer FS** — yuklangan media yo'qoladi → Cloudinary majburiy

---

## 13. HOZIRGI YARIM QOLGAN VAZIFA 🚧 (eng muhim — davom ettirish kerak)

**Foydalanuvchi maqsadi:** Loyihaga real start berish — barcha test datani o'chirib, real data qo'shishni boshlash.

**Bajarilgan:**
- ✅ `reset_for_launch` management command yozildi va `deploy` ga push qilindi (commit `ec624ce`)
  - Default: dry-run (sanaydi). `--confirm` bilan o'chiradi.
  - O'chiradi: hamma `TelegramUser`, `QRCode`, batch, `Store`, redemption, transaction, ticket, attempt, `Seller`, `SellerBatch`, loglar
  - Saqlaydi: `Gift` katalogi, viloyatlar, bannerlar, maxfiylik, tarjimalar, Django admin loginlari
  - `SellerRegistrationCode` ni reset qiladi (qayta ishlatish uchun)

**QOLGAN (keyingi agent bajarsin):**
1. 🔴 **`railway.json` + `Dockerfile.prod` dan `seed_test_data` ni olib tashlash** — aks holda keyingi deploy test datani qaytaradi! (8-bo'limga qarang)
2. ⏳ **Railway'ga login** kerak (`railway login` — interaktiv, foydalanuvchi qiladi). Hozir CLI token muddati tugagan.
3. ⏳ **Backup olish:** `railway run python manage.py backup_db` (o'chirishdan oldin xavfsizlik uchun)
4. ⏳ **Dry-run:** `railway run python manage.py reset_for_launch` (sonlarni ko'rish)
5. ⏳ **Tasdiqlangach o'chirish:** `railway run python manage.py reset_for_launch --confirm`
6. Tekshirish: admin panelда userlar/QR'lar 0 ekanini ko'rish

> **Eslatma:** Memory feedback bor — JIP loyihasidagi har bir muhim update **"JIP Development" Telegram guruhiga** yuborilishi kerak (terminalда kuzatish qiyin).

---

## 14. Keyingi qadamlar / yo'l xaritasi (oldingi sessiyalardan)

- Real API bog'lash (yangi admin SPA hozir mock data ishlatadi)
- Admin SPA da logo fix
- Webapp v5 ni production'da to'liq tekshirish
- Real do'konlar, sotuvchilar, QR partiyalarini kiritish

---

## 15. Foydali buyruqlar

```bash
# Lokal (agar venv sozlansa)
python manage.py runserver
python manage.py migrate
python manage.py shell

# Railway (login kerak)
railway login
railway link                                    # JIP service tanlash
railway run python manage.py <command>
railway logs

# Webapp lokal test (ngrok)
bash scripts/setup_ngrok.sh

# Admin SPA bundle qayta yig'ish
node scripts/build_admin_spa.js

# Deploy
git push origin deploy
```

---

## 16. Qo'shimcha hujjatlar (repo ichida)

- `README.md` — umumiy
- `SETUP.md` — lokal o'rnatish
- `PRODUCTION.md` — eski docker-compose deploy (Railway emas, eskirgan)
- `BUGS_FOUND.md` — to'liq bug ro'yxati + statuslar
- `DESIGN_TZ.md` — dizayn texnik topshirig'i
- `scripts/BACKUP_README_RU.md`, `scripts/CRONTAB_SETUP.md` — backup
- **`/JIP` skill** — Claude Code'da loyiha kontekstini tez yuklash uchun (memory'da ham bor)

---

*Tayyorladi: Claude (Opus 4.8). Savol bo'lsa — git tarixini va `core/models.py` ni birinchi o'qing.*
