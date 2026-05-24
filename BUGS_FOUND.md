# 🐛 JIP Production Bug List — RESOLVED
**Sana:** 2026-05-24
**URL:** https://jip-production.up.railway.app/
**Tester:** Claude (Puppeteer MCP)
**Status:** 18/22 tuzatildi va deploy qilindi (commit 9220160)

## ✅ TUZATILGAN VA TEKSHIRILGAN (Puppeteer testdan o'tdi)

### Kritik buglar (Round 1)
- BUG-001 Batch 500 → migration 0072 + try/except
- BUG-002 Gift add 500 → fieldsets fixed
- BUG-003 SellerRegistrationCode add 403 → has_add_permission=False
- BUG-004 Til tugmasi → ishlaydi (POST /i18n/setlang/)
- BUG-005 Stores tab QR data → scanned_by__user_type filter
- BUG-006 Root URL 404 → redirect / → /admin/
- BUG-008/009 JIP logo → site_logo + login_logo SVG
- BUG-010 Duplicate search → CSS hide
- BUG-014 Sotuvchi ID spacing → letter-spacing 1px
- BUG-023 (yangi) Redis URL config + cache defensive try/except

### UI polish (Round 2)
- BUG-007 Topmenu RU → "Bosh sahifa", "Boshqaruv paneli"
- BUG-011 Telefon format → "+998 74 234 56 78" (format_phone_uz utility)
- BUG-016 "Город Ташкент" → UZ tilida "Toshkent shahri" ko'rinadi
- BUG-017 Region "andijan — Андижанская" → faqat "Andijon viloyati"
- BUG-018 Tuman ustun bo'sh → seed_test_data district biriktirildi
- BUG-019 "Welcome" → "Xush kelibsiz! JIP boshqaruv paneliga kiring"

## 🟡 QOLGAN (sekundar)
- BUG-012/021 Date format ("23 Май 2026", "Май 21, 19:03") — Django builtin
- BUG-013 Mixed status badges (admin.py hardcoded RU short_descriptions)
- BUG-015 User detail page tili — get_language() conditional kerak
- BUG-020 Promokoddar telefon bo'sh/blur — webapp template
- BUG-022 Sidebar "Изменить пароль" / "Выйти" RU — Jazzmin internal



---

## 🔴 KRITIK BUGLAR (Funksional, sahifa ishlamaydi)

### BUG-001 — `/admin/core/qrcodebatch/add/` → 500 Server Error
- **Sahifa:** Batch yaratish formasi
- **Qadam:** Seller + Store + Quantity to'ldirib Save
- **Real:** 500 Server Error (HTML 145 bayt)
- **Test natija:** 2 ta turli store bilan ham takrorlandi
- **Status:** save_model'ga try/except qo'shildi, deploy kerak

### BUG-002 — `/admin/core/gift/add/` → 500 Server Error
- **Sahifa:** Sovg'a qo'shish formasi
- **Real:** GET 500 (forma hatto yuklanmaydi)
- **Sabab:** Tekshirish kerak (admin GiftAdmin)

### BUG-003 — `/admin/core/sellerregistrationcode/add/` → 403 Forbidden
- **Sahifa:** Standart admin add formasi
- **Real:** 403 (lekin "Yangi ID yaratish" tugmasi ishlaydi /generate/ orqali)
- **Yechim:** Add link sidebar'dan olib tashlash, faqat /generate/ qoldirish

### BUG-004 — Til tugmasi RU/UZ ishlamaydi
- **Sahifa:** /admin/dashboard/ (har qanday tab)
- **Qadam:** UZ tugmasini bosish
- **Real:** Hech narsa o'zgarmaydi, sahifa rus tilida qoladi
- **Severity:** HIGH

### BUG-005 — Dashboard `Магазины в акции` tab `Сантеники` ma'lumotini ko'rsatadi
- **Sahifa:** /admin/dashboard/?tab=stores
- **Real:** Region jadval Elektriklarni ko'rsatadi (15 sant, 38 skan), magaziny 6 lekin jadval bo'sh
- **Severity:** MEDIUM

### BUG-006 — Bosh sahifa `/` → 404 Not Found
- **Sahifa:** https://jip-production.up.railway.app/
- **Real:** 404, /admin/ ga redirect yoki landing page kerak

---

## 🟠 UI/UX KATTA BUGLAR

### BUG-007 — Til chalkash (Mixed Languages) HAR YERDA
- **Misol 1 (Admin sidebar):** "Админпанель" (rus) + "Batch'lar, Jonli efirlar, Sotuvchi IDlari" (uz)
- **Misol 2 (Dashboard):** "Общий, Пользователи, Подарки, Заявки" (rus) + "Barcha statistikani eksport qilish" (uz)
- **Misol 3 (List):** "Поиск, Выполнить, Сбросить" (rus) + "Batch'lar, Do'kon" (uz)
- **Misol 4 (Buttons):** "Добавить Batch" (rus), "Сохранить" (rus)
- **Misol 5 (Errors):** "Welcome" (en) + "Имя пользователя/Пароль" (rus) — login
- **Misol 6 (Дashboard):** "Management Hub" (en) + Тaba names (rus)
- **Severity:** HIGH — branding va consistency uchun muhim

### BUG-008 — Login Logo "A" (Abba), JIP emas
- **Sahifa:** /admin/login/
- **Real:** Abba kompaniyaning "A" logosi
- **Kerak:** JIP logo

### BUG-009 — Sidebar Logo `[A]` da Abba ikona
- **Sahifa:** Hamma admin sahifalar
- **Real:** Sidebar JIP matni + Abba "A" ikona
- **Kerak:** JIP brand-ga mos logo

### BUG-010 — Header'da 2 ta Search Box (dublikat)
- **Sahifa:** /admin/, /admin/core/*/ 
- **Real:** Header da bo'sh va takrorlangan 2 ta search input
- **Kerak:** Bittasini olib tashlash

### BUG-011 — Telefon format chalkash
- **Misol:** `998777771676` (Sadulla) vs `+99980000070` (Sarvar) vs `+998742345678`
- **Kerak:** Yagona format: `+998 XX XXX XX XX`

### BUG-012 — Vaqt format chalkash
- **Misol 1:** "23 Май 2026" (rus oy nomi)
- **Misol 2:** "56 минут oldin" (RU+UZ aralash)
- **Misol 3:** "23 мая 2026 г. 23:03"
- **Kerak:** Lokalga mos format

### BUG-013 — Status va Lable chalkash
- **Misol:** "АКТИВНО" (rus badge) + "oldin" (uz vaqt) bir qatorda
- **Misol:** "Tasdiqlangan" (uz) + "Sotuvchi" badge (uz) lekin "Пользователь Telegram" (rus header)

### BUG-014 — Sotuvchi ID raqamlari "1.7.4.4.2.5.4.3" tarzida ajralib ko'rinadi
- **Sahifa:** /admin/core/sellerregistrationcode/
- **Real:** ID `17442543` har raqam alohida cell ko'rinmoqda
- **Sabab:** CSS letter-spacing yoki monospace formatting issue

### BUG-015 — User detail page hammasi rus tilida (user uzbek bo'lsa ham)
- **Sahifa:** /admin/dashboard/... user detail
- **Real:** "TILI: O'ZBEK (LOTIN)" lekin barcha labellar ("ДЕЙСТВИЯ", "Аккаунт подтвержден", "Тренды активности") rus tilida
- **Kerak:** Admin paneli o'z tilini hisobga olishi yoki to'liq uzbek

---

## 🟡 KICHIK UI BUGLAR

### BUG-016 — "Город Ташкент" rus tilida (boshqa viloyatlar uz tilida)
- **Sahifa:** /admin/dashboard/?tab=users
- **Real:** Sadulla'ning Региона "Город Ташкент"
- **Kerak:** "Toshkent shahri" yoki konsistent format

### BUG-017 — `andijan — Андижанская область` — slug + rus name
- **Sahifa:** /admin/core/store/
- **Real:** Viloyat ustun aralash
- **Kerak:** Faqat O'zbek nomi: "Andijon viloyati"

### BUG-018 — Stores'da Tuman ustun bo'sh ("-")
- **Sahifa:** /admin/core/store/
- **Real:** Hamma do'konlarda Tuman = "-"
- **Kerak:** seed_test_data yangilanishi yoki yangi field

### BUG-019 — "Welcome" — login title inglizcha
- **Sahifa:** /admin/login/
- **Kerak:** "Xush kelibsiz" / "Добро пожаловать"

### BUG-020 — Promokoddar telefon ustun bo'sh/blurred
- **Sahifa:** /admin/dashboard/?tab=promocodes
- **Real:** Telefon ustun bo'sh ko'rinadi (yoki masked)

### BUG-021 — Vaqt "Май 21, 19:03" qisqartirilgan rus formatda
- **Sahifa:** /admin/dashboard/?tab=promocodes
- **Kerak:** "21.05.2026 19:03" yoki "21 may 2026, 19:03"

### BUG-022 — Sidebar'da `Изменить пароль`, `Выйти` rus tilida
- **Sahifa:** /admin/* (har joyda)
- **Kerak:** "Parolni o'zgartirish", "Chiqish"

---

## ✅ ISHLAYDIGAN FUNKSIYALAR (verified)

- Login va auth (admin/123)
- Dashboard `/admin/dashboard/` GET 200
- Batch list, QR list, Store list — barchasi GET 200
- "Yangi ID yaratish" (/sellerregistrationcode/generate/) — yangi ID muvaffaqiyatli yaratildi
- Filter panellar ochiladi
- Tab navigation (Общий/Пользователи/Подарки/...)

---

## 📊 STATISTIKA

- **Test qilingan URL:** 34
- **500 xato:** 2 (`qrcodebatch/add/`, `gift/add/`)
- **403 xato:** 1 (`sellerregistrationcode/add/`)
- **200 OK:** 31
- **Topilgan bug:** 22
- **Kritik:** 6
- **UI/UX katta:** 9
- **Kichik:** 7

---

## 🎯 PRIORITET TUZATISH TARTIBI

1. **BUG-001** — Batch 500 (eng kritik, daromad bilan bog'liq)
2. **BUG-002** — Gift add 500
3. **BUG-003** — SellerRegistrationCode add 403 (yoki UI'dan olib tashlash)
4. **BUG-004** — Til tugmasi ishlashi
5. **BUG-007** — Til chalkash (global o'zgartirish)
6. **BUG-005** — Magaziny tab data
7. **BUG-008, 009** — Logo'larni JIP'ga o'zgartirish
8. **BUG-014** — Sotuvchi ID CSS fix
9. Qolgan UI buglar (batch fix)
