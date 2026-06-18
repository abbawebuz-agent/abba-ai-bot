# JIP Dashboard — To'liq Realizatsiya Rejasi

> **Maqsad:** Loyihadagi BARCHA datani bitta qulay, chiroyli dashboardda ko'rish va analiz qilish.
> **Holat:** Reja (dizayn Claude Design'da chiziladi, keyin men implement qilaman).
> **Qoida:** Django admin paneliga (`/admin/`) UMUMAN tegilmaydi. DB'ga test data/promokod qo'shilmaydi, hech narsa o'chirilmaydi. Dashboard FAQAT-O'QISH (read-only) + eksport.

> ### ✅ TASDIQLANGAN QARORLAR (2026-06-17)
> 1. **Funksional doira:** FAQAT-O'QISH — ko'rish + analiz + eksport. Status o'zgartirish/sotuvchi tasdiqlash kabi YOZISH amallari admin panelda qoladi. DB'ga hech narsa yozilmaydi.
> 2. **Til:** UZ (default) + RU, toggle bilan.
> 3. **Tartib:** Sahifalar A→K ketma-ket ishlab chiqiladi (avtonom). Avval API qatlami, keyin SPA skeleton, keyin har sahifa.
> 4. **Keyingi qadam:** Foydalanuvchi rejani o'rganadi → Claude Design'da dizayn chizadi → MEN implement qilaman. Dizayn kelguncha kod yozilmaydi.

---

## 0. Texnik arxitektura

| Element | Yechim |
|---------|--------|
| **URL** | `/jip-admin/` (mavjud SPA shu yerda — to'liq qayta quramiz) |
| **Auth** | Django staff login (`@staff_member_required`) — mavjud |
| **Frontend** | React 18 + Babel (CDN, build step yo'q) — webapp bilan bir uslub, yoki dizaynerga qarab |
| **API** | YANGI read-only JSON endpointlar: `/jip-admin/api/...` (admin URL'lariga tegmaymiz) |
| **Analitika** | `core/dashboard_stats.py` dagi `compute_*` funksiyalar QAYTA ishlatiladi (admin bilan bir manba → raqamlar mos keladi) |
| **Grafik** | Chart.js (CDN) |
| **Real-time** | YO'Q (har yuklanishda yangi so'rov; ixtiyoriy auto-refresh 60s) |
| **Yozish operatsiyalari** | YO'Q (faqat ko'rish + eksport). Statusni o'zgartirish kabi amallar admin panelda qoladi. |

**MUHIM:** Dashboard hech qachon DB'ga yozmaydi. Faqat `SELECT` + eksport. Bu xavfsizlik va "data buzilmasin" qoidasiga to'liq mos.

---

## 1. Global Layout (har sahifada bor)

### 1.1. Chap Sidebar (navigatsiya) — 11 bo'lim
```
┌─ JIP DASHBOARD ────────┐
│ 📊 Umumiy ko'rinish     │  ← Overview (home)
│ 👥 Foydalanuvchilar     │  ← Users (santenik + sotuvchi)
│ 🎟  Promokodlar         │  ← QR / skretch kartalar
│ 🎁 Sovg'alar            │  ← Gift katalog + so'rovlar
│ 🏪 Sotuvchilar          │  ← Seller + partiyalar + balans
│ 🗺  Geografiya          │  ← Viloyat/tuman drill-down
│ 🛡  Xavfsizlik (Fraud)  │  ← Promokod urinishlari, bloklar
│ 📣 Rassilkalar          │  ← Broadcast + region + oylik
│ 🏆 Lotereya / Efir      │  ← MonthlyPromoTicket + LiveStream
│ 🖼  Loyiha rasmlari     │  ← ProjectPhoto galereya
│ 📜 Audit log            │  ← ActivityLog
├────────────────────────┤
│ ⚙️  Admin panelga o'tish│  ← /admin/ ga link (yangi tab)
│ 🚪 Chiqish              │
└────────────────────────┘
```

### 1.2. Yuqori Topbar (har sahifada)
- **Sana filtri (global):** `7 kun` · `1 oy` · `O'tgan oy` · `Hamma vaqt` · `Maxsus diapazon (date_from → date_to)`
  - Bu filtr URL query'ga yoziladi (`?from=...&to=...`), barcha KPI/grafik shunga moslanadi
  - Manba: `_resolve_dashboard_dates()` mantiqi
- **Til toggle:** UZ / RU (interfeys tili)
- **Yangilash tugmasi** (🔄) — qayta yuklash
- **Eksport tugmasi** (📥) — joriy sahifa ma'lumotini Excel/CSV
- **Foydalanuvchi:** admin ismi + chiqish

### 1.3. Umumiy komponentlar
- **KPI karta:** sarlavha + katta raqam + trend strelka (▲ +12% / ▼ -5%) + kichik subtitle
- **Grafik karta:** sarlavha + Chart.js + legend
- **Jadval:** saralash (ustun bosilganda), paginatsiya, qidiruv, satr bosilsa → detal
- **Filter chip'lar:** user_type, region, status — bosilganda qo'shiladi/olib tashlanadi
- **Empty state:** data yo'q bo'lsa chiroyli xabar

---

## 2. SAHIFA A — 📊 Umumiy ko'rinish (Overview / Home)

**Maqsad:** Bir qarashda butun tizim holati.
**Data manbai:** `compute_general_stats()`, `compute_dashboard_charts()`, `compute_intelligence_stats()`

### 2.1. KPI kartalar qatori (yuqorida, 8 ta)
| # | Karta | Qiymat | Trend | Manba |
|---|-------|--------|-------|-------|
| 1 | Jami foydalanuvchi | `life_u_total` | ▲ davr o'sishi (`trends.users_total`) | TelegramUser |
| 2 | Santexniklar | `life_u_e` | — | user_type=santenik |
| 3 | Sotuvchilar | `life_u_s` | — | user_type=sotuvchi |
| 4 | Rol tanlamagan | `life_u_unselected` | — | user_type bo'sh |
| 5 | Jami promokod | `life_qr_e_total` | — | QRCode (is_deleted=False) |
| 6 | Skanlangan promokod | `life_qr_e_scanned` | aktivatsiya % | is_scanned=True |
| 7 | Tarqatilgan ball | `life_points_total` | ▲ (`trends.points_total`) | Sum(points) scanned |
| 8 | Kutilayotgan sovg'a so'rovi | `gifts_pending` | — | GiftRedemption status=pending |

### 2.2. Grafiklar qatori (3 ta line/area chart)
1. **Ro'yxatdan o'tishlar trendi** — kunlik yangi userlar (line). Manba: `charts` reg_series
2. **Promokod aktivatsiyasi trendi** — kunlik skanlar + ball (dual line). Manba: act_series + act_pts_series
3. **Sovg'a so'rovlari trendi** — kunlik redemption + ball (line). Manba: red_series + red_pts_series

### 2.3. Pastki blok (2 ustun)
- **Chap:** Sovg'a so'rovlari status taqsimoti (donut chart): pending/approved/sent/completed/rejected/cancelled/not_received. Manba: `redemption_stats`
- **O'ng:** Foydalanuvchi integritet segmentlari (donut): clean / warning / suspicious / blocked. Manba: `intelligence_stats.segments`

### 2.4. Tugmalar/interaktiv
- Har KPI karta bosilsa → tegishli sahifaga o'tadi (masalan "Santexniklar" → Users sahifasi santenik filtri bilan)
- Grafik nuqtasi hover → tooltip (sana + qiymat)
- Sana filtri o'zgarsa → hamma qayta hisoblanadi

---

## 3. SAHIFA B — 👥 Foydalanuvchilar (Users)

**Maqsad:** Barcha foydalanuvchilarni ko'rish, filtrlash, qidirish, har birining detali.
**Data manbai:** `TelegramUser` (select_related region/district)

### 3.1. KPI kartalar (4 ta)
- Jami / Santexnik / Sotuvchi / Bugun qo'shilgan (created_at=today)

### 3.2. Filtrlar paneli
| Filtr | Variantlar | Manba field |
|-------|-----------|-------------|
| Qidiruv | ism/familiya/username/telefon | `Q(...icontains)` |
| Rol | Hammasi / Santexnik / Sotuvchi / Rol tanlamagan | user_type |
| Viloyat | dropdown (UzRegion ro'yxati + "Noma'lum") | region__code |
| Til | Hammasi / UZ / RU | language |
| Faollik | Faol / Nofaol | is_active |
| Ro'yxat holati | Tugallangan / Tugallanmagan | privacy+phone+region |
| Sana | global filtr (created_at) | created_at |
| Saralash | Sana / Ball / Ism (▲▼) | ordering |

### 3.3. Jadval ustunlari
| Ustun | Manba |
|-------|-------|
| ID / Avatar | telegram_id |
| Ism Familiya | first_name + last_name |
| @username | username |
| Telefon | phone_number |
| Rol | user_type (badge) |
| Viloyat / Tuman | region / district (yoki district_custom) |
| Ball | points |
| Til | language |
| Ro'yxat | ✅/⏳ (is_registration_complete) |
| Holat | Faol/Bloklangan (is_active, promo_blocked_until) |
| Qo'shilgan | created_at |

- **Paginatsiya:** 20/sahifa
- **Satr bosilsa →** Foydalanuvchi detal modal/sahifa (3.4)

### 3.4. Foydalanuvchi DETAL (satr bosilganda)
**Manba:** `user_detail_view` mantiqi (mavjud)
- Profil: ism, telefon, @username, TG ID, til, viloyat/tuman, ro'yxat sanasi, status
- Ball: joriy balans (`calculate_points`), welcome bonus berilganmi
- **Skanlagan promokodlar** jadvali: kod, serial, ball, sana (scanned_qrcodes)
- **Sovg'a so'rovlari** jadvali: sovg'a, status, ball, sana (gift_redemptions)
- **Promokod urinishlari** (fraud): muvaffaqiyatli/xato, manba, sana (promo_code_attempts)
- **Loyiha rasmlari** galereya (project_photos)
- **Bloklanish:** promo_failed_attempts, promo_blocked_until
- Sotuvchi bo'lsa: seller_approved, tranzaksiyalar, partiyalar
- **Tugmalar:** "Admin panelda ochish" (link, yangi tab) — tahrirlash admin'da

### 3.5. Tugmalar
- 📥 Eksport (joriy filtr bo'yicha Excel)
- Filtr tozalash
- Detal: faqat ko'rish + admin'ga link

---

## 4. SAHIFA C — 🎟 Promokodlar (QR / skretch kartalar)

**Maqsad:** Barcha promokodlarni ko'rish, qaysi usta skanlaganini analiz qilish.
**Data manbai:** `QRCode` (is_deleted=False)

### 4.1. KPI kartalar (5 ta)
- Jami promokod / Skanlangan / Skanlanmagan / Aktivatsiya % / Jami ball pool

### 4.2. Filtrlar
- Qidiruv: kod / serial / hash / skanlovchi ism-telefon
- Holat: Skanlangan / Skanlanmagan
- Partiya (batch) dropdown
- Sotuvchi dropdown (SellerBatch range bo'yicha)
- Viloyat (skanlovchi userning)
- Sana (scanned_at)
- Saralash: scanned_at / sequence_number

### 4.3. Jadval
| Ustun | Manba |
|-------|-------|
| Tartib № | sequence_number |
| Kod | code (S+7) |
| Serial | serial_number |
| Ball | points |
| Holat | is_scanned (✅/⬜) |
| Kim skanladi | scanned_by (ism + telefon) |
| Skanlangan sana | scanned_at |
| Partiya | batch.name |

- **Satr bosilsa →** promokod detali: skanlovchi profil + skanlangan vaqt + lotereya bileti bormi (MonthlyPromoTicket). Manba: `promo_qr_detail` + `_promo_qr_winner_context`

### 4.4. Grafik
- Kunlik aktivatsiya trendi (allaqachon Overview'da bor — bu yerda batafsil + ball)
- Partiyalar bo'yicha aktivatsiya % (bar chart)

### 4.5. Tugmalar
- 📥 Eksport
- Partiya tanlab → o'sha partiya kodlari

---

## 5. SAHIFA D — 🎁 Sovg'alar va So'rovlar

**Maqsad:** Sovg'a katalogi + barcha so'rovlarni status bo'yicha kuzatish.

### 5.1. Ikki sub-tab: **Katalog** | **So'rovlar**

#### 5.1.A. Katalog (Gift)
- Grid: rasm, nom (UZ/RU), ball narxi, zaxira (stock_quantity yoki "cheksiz"), faol/nofaol, tartib
- KPI: jami sovg'a / faol / nechta so'ralgan
- Har sovg'a bosilsa: nechta marta so'ralgan, qaysi statuslar (redemptions count)
- Filtr: qidiruv (nom), faqat faol

#### 5.1.B. So'rovlar (GiftRedemption)
**Data manbai:** `redemption_stats` + jadval
- **KPI banner (8 status):** Jami / pending / approved / sent / completed / rejected / cancelled / not_received + **Sarflangan ball** (completed)
- **Status taqsimoti** (donut/bar)
- Filtrlar: qidiruv (user/gift), status, user_type, viloyat, sana (requested_at)
- Jadval: foydalanuvchi, sovg'a, ball narxi, status (badge), so'ralgan sana, tasdiqlangan, izoh
- Satr bosilsa: to'liq detal (user profil + gift + status tarixi)

### 5.2. Tugmalar
- 📥 Eksport (so'rovlar)
- Status filtr chip'lar

---

## 6. SAHIFA E — 🏪 Sotuvchilar (Sellers)

**Maqsad:** Sotuvchilar, ularning promokod partiyalari, balans tranzaksiyalari.
**Data manbai:** `Seller`, `SellerBatch`, `SellerPointsTransaction`, `build_promo_table_rows('seller')`, `compute_store_analytics()`

### 6.1. KPI kartalar
- Jami sotuvchi / Tasdiqlangan / Tasdiqlanmagan (zaproslar) / Jami berilgan promokod / Jami aktivatsiya %

### 6.2. Sotuvchilar jadvali (`build_promo_table_rows`)
| Ustun | Manba |
|-------|-------|
| Sotuvchi nomi | Seller.name |
| Telefon | phone |
| Viloyat/Tuman | region/district |
| Partiyalar soni | seller_batches.count |
| Jami promokod | total_promos() |
| Aktivlashtirilgan | activated_count() |
| Aktivatsiya % | activation_percent() |
| Jami ball | total_points() |

- Satr bosilsa → Sotuvchi detal:
  - **Partiyalar** (SellerBatch): #from–#to diapazon, soni, aktivatsiya %
  - **Tranzaksiyalar** (SellerPointsTransaction): tur, ball (+/-), sotuv summasi $, davr, izoh, kim qo'shgan, sana
  - **Balans grafigi** (kümülativ)

### 6.3. Sub-tab: **Tasdiqlanmagan sotuvchilar (Zaproslar)**
- TelegramUser user_type=sotuvchi, seller_approved=False
- Faqat ko'rish (tasdiqlash admin panelda)

### 6.4. Tugmalar
- 📥 Eksport
- Detal → admin'ga link

---

## 7. SAHIFA F — 🗺 Geografiya (Regions / Districts)

**Maqsad:** Viloyat → tuman bo'yicha drill-down analiz.
**Data manbai:** `build_promo_table_rows` (region bo'yicha), drill_region/district mantiq

### 7.1. Yuqorida: O'zbekiston xaritasi (yoki viloyatlar bar chart)
- Har viloyat: foydalanuvchi soni / skanlar / ball (rang intensivligi = aktivlik)
- Viloyat bosilsa → tumanlar darajasiga drill-down

### 7.2. Viloyatlar jadvali
| Ustun | Manba |
|-------|-------|
| Viloyat | UzRegion.name |
| Foydalanuvchi | count |
| Skretch/promokod skanlar | scanned_cards |
| Ball | points |
| Sarflangan ball | spent |

### 7.3. Drill-down: viloyat → tumanlar → foydalanuvchilar ro'yxati
- "Noma'lum" (region=null) alohida ko'rsatiladi
- Manba: `dashboard_view` ichidagi `drill_region` + `selected_district` mantiq

### 7.4. Tugmalar
- Viloyat/tuman tanlash (breadcrumb: O'zbekiston > Toshkent > Chilonzor)
- 📥 Eksport

---

## 8. SAHIFA G — 🛡 Xavfsizlik / Fraud (Intelligence)

**Maqsad:** Firibgarlik aniqlash, bloklangan userlar, urinishlar analizi.
**Data manbai:** `compute_intelligence_stats()`, `PromoCodeAttempt`

### 8.1. KPI kartalar
- Jami urinish / Muvaffaqiyatli / Xato / Muvaffaqiyat % / O'rtacha kunlik xato / Bloklangan user soni

### 8.2. Integritet segmentlari (donut + ro'yxat)
- **Clean** (0 xato) / **Warning** (1-2 xato) / **Suspicious** (3+ xato) / **Blocked** (promo_blocked_until > now)
- Manba: `segments`

### 8.3. Shubhali faollik leaderboard (Top 10)
- Ism, telefon, ketma-ket xato soni (promo_failed_attempts)
- Manba: `leaderboard`

### 8.4. Grafiklar
- **Kunlik anomaliya trendi:** muvaffaqiyatli vs xato (dual line). Manba: `trends`
- **Manba taqsimoti:** bot vs webapp vs unknown (pie). Manba: `sources`

### 8.5. Urinishlar jadvali (PromoCodeAttempt)
- Foydalanuvchi, kiritilgan kod (raw_code), muvaffaqiyatli/xato, manba, sana
- Filtr: muvaffaqiyatli/xato, manba, sana

### 8.6. Tugmalar
- 📥 Eksport
- User bosilsa → User detal

---

## 9. SAHIFA H — 📣 Rassilkalar (Broadcasts)

**Maqsad:** Yuborilgan barcha xabarlar tarixi va natijasi.
**Data manbai:** `BroadcastMessage`, `RegionMessageLog`, `MonthlyReminderLog`

### 9.1. Sub-tablar: **Umumiy rassilka** | **Viloyat bo'yicha** | **Oylik eslatma**

#### Umumiy (BroadcastMessage)
- Jadval: nom, matn (qisqa), filtr (user_type/region/language/store), holat (pending/sending/completed/failed), jami/yuborildi/xato, sana
- KPI: jami rassilka / yuborilgan xabar / muvaffaqiyat %

#### Viloyat bo'yicha (RegionMessageLog)
- Jadval: viloyat, filtrlar, jami/yuborildi/xato, holat, kim yubordi, sana, rejalashtirilgan vaqt

#### Oylik eslatma (MonthlyReminderLog + Settings)
- Sozlama holati (yoqilgan/o'chirilgan, vaqt)
- Loglar: oy, jami/yuborildi/xato, status

### 9.2. Tugmalar
- 📥 Eksport
- Faqat ko'rish (yuborish admin panelda)

---

## 10. SAHIFA I — 🏆 Lotereya / Jonli Efir

**Maqsad:** Oylik lotereya biletlari + jonli efir g'oliblari.
**Data manbai:** `MonthlyPromoTicket`, `LiveStream`, `LiveStreamWinner`

### 10.1. Sub-tab: **Lotereya biletlari** | **Jonli efirlar**

#### Lotereya (MonthlyPromoTicket)
- KPI: joriy oy biletlari / jami biletlar / ishtirokchi userlar
- Oy bo'yicha filtr
- Jadval: bilet №, foydalanuvchi, user_type, skanlangan QR, sana
- Foydalanuvchi bo'yicha shanslar soni (count) — top ishtirokchilar
- Grafik: oylar bo'yicha bilet soni

#### Jonli efirlar (LiveStream)
- Kartalar: sarlavha, efir vaqti, ishtirokchi soni, o'tgan/kelgusi
- Har efir → g'oliblar ro'yxati (LiveStreamWinner): foydalanuvchi, sovg'a, o'rin

### 10.2. Tugmalar
- 📥 Eksport
- Oy/efir tanlash

---

## 11. SAHIFA J — 🖼 Loyiha rasmlari (ProjectPhoto)

**Maqsad:** Ustalar yuklagan ish rasmlarini ko'rish (real ekanini tasdiqlash).
**Data manbai:** `ProjectPhoto`

### 11.1. KPI
- Jami rasm / Faol (is_deleted=False) / Usta o'chirgan / Bugun yuklangan

### 11.2. Galereya (grid)
- Rasm thumbnail + izoh (caption) + usta ism + sana
- Filtr: usta bo'yicha, faqat faol / o'chirilgan, sana
- Rasm bosilsa → katta ko'rinish + usta profil linki

### 11.3. Tugmalar
- 📥 Eksport (metadata)
- Faqat ko'rish

> ⚠️ Eslatma: rasm fayllari Railway efemer FS'da yo'qolishi mumkin (Cloudinary pending). Thumbnail 404 bo'lsa fallback ikonka.

---

## 12. SAHIFA K — 📜 Audit Log (ActivityLog)

**Maqsad:** Tizimdagi barcha amallar tarixi.
**Data manbai:** `ActivityLog`

### 12.1. KPI
- Jami log / Bugungi amallar / Kirish urinishlari / Xatolar

### 12.2. Filtrlar
- Amal turi (login/create/update/delete/backup/export/webhook/error...)
- Kim (admin user)
- Obyekt turi (target_model)
- Sana

### 12.3. Jadval
- Vaqt, Kim (admin/TG user), Amal turi (badge+emoji), Obyekt (target_repr), Tavsif, IP, Brauzer
- Satr bosilsa → metadata (JSON) ko'rinadi

### 12.4. Tugmalar
- 📥 Eksport
- Faqat ko'rish (o'chirilmaydi — immutable jurnal)

---

## 13. Eksport tizimi (barcha sahifalarda)

- Har sahifada 📥 tugma → joriy filtr/saralash bo'yicha **Excel (.xlsx)** yoki **CSV**
- Manba: `openpyxl` (loyihada bor — `core/utils.py:build_promo_batch_xlsx`)
- Yangi endpoint: `/jip-admin/api/export/<section>/?<filtrlar>`
- DB'ga yozmaydi, faqat o'qiydi va fayl qaytaradi

---

## 14. API endpointlar ro'yxati (yangi, read-only)

> Hammasi `/jip-admin/api/` ostida, `@staff_member_required`, GET, JSON. Admin URL'lariga TEGMAYDI.

| Endpoint | Vazifa | Manba funksiya |
|----------|--------|----------------|
| `GET /jip-admin/api/overview/?from&to` | Overview KPI + grafik | compute_general_stats + charts + intelligence |
| `GET /jip-admin/api/users/?q&type&region&...&page` | Foydalanuvchilar ro'yxati | TelegramUser |
| `GET /jip-admin/api/users/<id>/` | User detal | user_detail mantiq |
| `GET /jip-admin/api/promocodes/?...&page` | Promokodlar | QRCode |
| `GET /jip-admin/api/promocodes/<id>/` | Promokod detal | QRCode + ticket |
| `GET /jip-admin/api/gifts/` | Sovg'a katalog | Gift |
| `GET /jip-admin/api/redemptions/?...&page` | So'rovlar | GiftRedemption |
| `GET /jip-admin/api/sellers/?...` | Sotuvchilar | build_promo_table_rows |
| `GET /jip-admin/api/sellers/<id>/` | Sotuvchi detal | Seller+batch+txn |
| `GET /jip-admin/api/geo/?region&district` | Geografiya drill | build_promo_table_rows |
| `GET /jip-admin/api/fraud/?from&to` | Fraud analitika | compute_intelligence_stats |
| `GET /jip-admin/api/broadcasts/?type` | Rassilkalar | Broadcast/Region/Monthly logs |
| `GET /jip-admin/api/lottery/?month` | Lotereya biletlari | MonthlyPromoTicket |
| `GET /jip-admin/api/livestreams/` | Jonli efirlar | LiveStream + Winner |
| `GET /jip-admin/api/projects/?user&page` | Loyiha rasmlari | ProjectPhoto |
| `GET /jip-admin/api/audit/?...&page` | Audit log | ActivityLog |
| `GET /jip-admin/api/export/<section>/?...` | Excel/CSV eksport | openpyxl |
| `GET /jip-admin/api/filters/` | Dropdown ma'lumotlari (viloyatlar, sotuvchilar, partiyalar) | UzRegion/Seller/Batch |

---

## 15. Dizayn uchun eslatmalar (Claude Design)

- **Tillar:** UZ (default) + RU — interfeys ikkala tilda
- **Adaptiv:** desktop birinchi (admin ekranida ishlatiladi), lekin planshet ham
- **Ranglar:** JIP brend (webapp ko'k `#0B63F6` yoki dizayner tanlovi)
- **Komponentlar:** KPI karta, grafik karta (Chart.js), jadval (saralash+paginatsiya), filter paneli, donut/line/bar chartlar, detal modal/drawer, breadcrumb (geografiya), badge (status/rol), empty state
- **Navigatsiya:** chap sidebar (yig'iladigan) + yuqori topbar (global sana filtri)
- **Trend ko'rsatkichlari:** ▲ yashil (o'sish) / ▼ qizil (kamayish)

---

## 16. Implementatsiya bosqichlari (dizayn tayyor bo'lgach)

1. **API qatlami** — `core/dashboard_api.py` (yangi fayl), `compute_*` qayta ishlatib JSON endpointlar. URL: `mona/urls.py` ga `/jip-admin/api/...` qo'shish (admin URL'lariga tegmasdan).
2. **SPA skeleton** — `templates/jip_admin/index.html` to'liq qayta yoziladi (React + router), sidebar + topbar + sana filtri.
3. **Sahifalar** — har birini ketma-ket (Overview → Users → ... → Audit).
4. **Grafiklar** — Chart.js integratsiya.
5. **Eksport** — Excel/CSV endpointlar.
6. **Test** — har sahifa real data bilan (lokal/prod read-only), 0 ta 500 (curl sweep qoidasi).
7. **Deploy** — `git push origin deploy`.

> Har bosqichda DB'ga yozilmaydi, admin panel o'zgartirilmaydi.

---

## 17. DATA INVENTARI (to'liq — nima borligi)

| Model | Asosiy maydonlar | Dashboard'da qayerda |
|-------|------------------|----------------------|
| TelegramUser | telegram_id, ism, telefon, region/district, points, language, user_type, is_active, privacy, seller_approved, promo_blocked_until, created_at | Users, Overview, Geo, Fraud |
| QRCode | code, serial, sequence_number, points, is_scanned, scanned_by, scanned_at, batch, is_deleted | Promokodlar, Overview |
| QRCodeBatch | name, seller, quantity, points_per_code, status, delivery_status, created_at | Promokodlar (partiya), Sotuvchilar |
| Gift | name_uz/ru, points_cost, stock_quantity, is_active, image, order | Sovg'alar katalog |
| GiftRedemption | user, gift, status(7), requested_at, confirmed_at, user_comment | Sovg'alar so'rovlar, Overview |
| Seller | name, phone, region/district, notes | Sotuvchilar |
| SellerBatch | seller, promo_from, promo_to | Sotuvchilar (partiya) |
| SellerPointsTransaction | seller, points, type, sales_amount_usd, period, note | Sotuvchilar (balans) |
| MonthlyPromoTicket | month, qr_code, user, user_type, order, scanned_at | Lotereya |
| LiveStream | title, scheduled_at, stream_url, participants_count | Jonli efir |
| LiveStreamWinner | live_stream, user, prize_text, position | Jonli efir |
| ProjectPhoto | user, image, caption, is_deleted, created_at | Loyiha rasmlari |
| PromoCodeAttempt | user, raw_code, is_successful, source, attempted_at | Fraud |
| BroadcastMessage | title, message_text, filtrlar, status, sent/failed | Rassilkalar |
| RegionMessageLog | region_code, total/sent/failed, status, scheduled_at | Rassilkalar |
| MonthlyReminderLog | month_key, total/sent/failed, status | Rassilkalar |
| ActivityLog | timestamp, user, action_type, target, description, ip | Audit |
| Promotion | title, image, link, date, is_active | (ixtiyoriy — Sozlamalar) |
| UzRegion / UzDistrict | code, name_uz/ru | Geo, filtrlar |
| Store | name, region, owner (deprecated) | (ixtiyoriy) |
| AdminContactSettings, PrivacyPolicy, VideoInstruction | sozlamalar | (ixtiyoriy — Sozlamalar sahifasi) |
