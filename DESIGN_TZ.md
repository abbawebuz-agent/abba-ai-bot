# 🎨 TZ — JIP Loyalty WebApp Redesign

**Loyiha:** JIP Loyalty Platform — Telegram Mini App
**Mahsulot turi:** Loyallik dasturi (B2B + B2C)
**Maqsad:** Telegram orqali ochiladigan 2 ta WebApp (Sotuvchi va Santexnik)
**Hozirgi holat:** Funksional ammo dizayn "yengil/oddiy" — chuqurlik yo'q, kontrast past, kartalar bir xilday
**Texnologiya:** HTML + CSS + vanilla JS (Telegram WebApp SDK, Chart.js)

---

## 🎯 Maqsadli auditoriya

### Sotuvchi (B2B)
- **Kim:** Santexnika do'koni egasi/menejeri (Sa'dulla kabi)
- **Yosh:** 28–55
- **Texnik level:** O'rtacha (Telegram bilan ishlaydi, lekin murakkab UI tushunmaydi)
- **Kontekst:** Ish vaqtida do'konda telefonda tezroq tekshirish — balansim, kim ko'p sotgan, qancha komissiya tushgan
- **Asosiy emotsional ehtiyoj:** "Mening biznesim qanday ketyapti?" — ishonch, professional ko'rinish, raqamlar aniq

### Santexnik (B2C — santexnik mutaxassis)
- **Kim:** Mahalliy santexnik (uy santexnikasi, qurilish ustasi)
- **Yosh:** 22–45
- **Texnik level:** Past–o'rtacha (asosan telefondan)
- **Kontekst:** Do'kondan tovar olgach QR-kodni skan qiladi → ball oladi → ballarga sovg'a tanlaydi
- **Asosiy emotsional ehtiyoj:** "Qancha ball yig'dim, qaysi sovg'aga yetdi?" — o'yin, mukofot, progress

---

## 🧭 Brand va atmosfera

### Brand qiymatlari
- **Trust** (ishonch) — yirik B2B brand sifatida ko'rinish
- **Modern** (zamonaviy) — eski "Soviet" tipografiya emas, **fintech / SaaS** dizayni
- **Local** (mahalliy) — O'zbek tili birinchi, Rus tili ikkinchi
- **Approachable** (yaqin) — texnik bo'lmaganlar ham tushunsin

### Hozirgi logo
```
JIP LOYALTY
[💎 ko'k+ko'k-yashil olmos shaklida ikona]
```
Logo to'g'ri yaratilgan — saqlanadi.

### Tavsiya etiladigan palitra (siz boshqa variant taklif qila olasiz)

**Primary palette (asosiy ko'k):**
- `#1d4ed8` — chuqur ko'k (asosiy)
- `#2563eb` — ko'k (CTA tugma)
- `#3b82f6` — yengil ko'k (hover)
- `#06b6d4` — cyan (gradient accent)
- `#dbeafe` → `#eff6ff` — light bg

**Neutral palette:**
- `#0f172a` — text dark
- `#475569` — text muted
- `#94a3b8` — text light
- `#e2e8f0` — border
- `#f1f5f9` — bg card
- `#f8fafc` — bg page

**Semantic:**
- `#10b981` / `#d1fae5` — success (ball qo'shildi, sovg'a tasdiqlandi)
- `#f59e0b` / `#fef3c7` — warning (kutilmoqda, low stock)
- `#ef4444` / `#fee2e2` — error (rad etildi, xato)

### Tipografiya
- **Hozir:** `-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Inter', sans-serif`
- **Tavsiya:** Inter (yoki SF Pro / system fonts) — clean modern fintech
- **Sizes (mobile 375px):**
  - Display (balance): 36–42px / 800
  - Title: 18–22px / 700
  - Body: 14–15px / 500
  - Caption: 11–12px / 600 (uppercase)

### Border-radius
- Cards: 14–18px (yumshoq lekin haddan ortiq emas)
- Buttons: 10–12px
- Pills/badges: 100px (to'liq yumaloq)

### Shadow / Depth
- Cards: `0 2px 8px rgba(0,0,0,0.04)` (subtle)
- Hero cards: `0 12px 32px rgba(37,99,235,0.25)` (premium feel)
- Bottom tab bar: `0 -4px 24px rgba(0,0,0,0.06)`

### Iconography
- Outlined SVG (stroke-width 2–2.5)
- Telegram emoji'lar (📦 💰 🏪) ham OK ammo — **icon + text** bir vaqtda yumshoqroq
- Tavsiya: **Lucide Icons** yoki **Heroicons** kutubxonasi

---

## 📱 EKRAN-EKRAN dizayn briefi

### Konteynerni tushunish — Telegram Mini App constraint:
- **Width:** 100% mobile (320–428px), tablet 600px center
- **Height:** Telegram WebApp expand → full screen
- **Bottom 80px safe area** uchun (custom bottom tab bar)
- **Top 0** — Telegram nativ MainButton/BackButton yo'q (skipped)
- **Dark mode auto** — `var(--tg-theme-bg-color)` qo'llab-quvvatlash

---

## 🛒 1-WEBAPP: SOTUVCHI PANELI

**URL:** `/api/webapp/seller/`
**Foydalanuvchi:** Santexnika do'koni egasi (admin tasdiqlagan)
**Tab soni:** 5 (bottom bar)

### Tab 1: 🏠 Bosh sahifa (Dashboard)

**Maqsad:** Bir qarashda biznes holati

**Tarkib (yuqoridan pastga):**
1. **Hero balance card** — gradient ko'k-cyan, 200px+ balandlik
   - Yuqorida label: "💰 Joriy balans" (uppercase 11px, opacity 0.85)
   - Asosiy raqam: `12,450 ball` (36–42px, 800)
   - Delta pill: `↗ +850 (30 kun)` yoki `↘ -200 (30 kun)` (yumaloq pill, semi-transparent oq)
   - Pastda hint: "Ballar admin tomonidan batch yaratganda qo'shiladi" (11px, opacity 0.7)
   - **Idea:** decorative blob shape orqa fonda (visual interest)

2. **Balans tarixi grafigi** — 30 kunlik kumulyativ
   - Card (border-radius 14, padding 14)
   - Header: "📈 Balans tarixi" + pill "Oxirgi 30 kun"
   - Line chart (Chart.js): gradient fill (cyan to transparent)
   - Tooltip on touch: kun + ball
   - **Idea:** sparkline-like minimal, ortiqcha grid line emas

3. **4 ta stat card** — 2x2 grid (mobile) / 4x1 (tablet)
   - "📦 Jami QR" — soni
   - "✅ Skanlangan" — soni
   - "📊 Aktivatsiya %" — rang status: yashil >50, sariq 20–50, qizil <20
   - "💳 Komissiya %"

4. **Do'kon info card** — list style
   - Nomi, Viloyat, Manzil
   - Tahrir tugmasi (ixtiyoriy MVP+)

**UX qoidalar:**
- Yuqorida refresh tugma (header right) — bosilganda spinner + reload
- Pull-to-refresh (mobile native) — agar imkoniyat bo'lsa
- Loading state: skeleton shimmer, "Yuklanmoqda..." text emas

---

### Tab 2: 💰 Ballar (Tranzaksiyalar)

**Maqsad:** Har bir ball qaerdan kelganini ko'rish

**Tarkib:**
1. Filter chips (yuqorida) — gorizontal scroll bo'lsa
   - "Hammasi" (active)
   - "+ Qo'shildi"
   - "- Ayirildi"
2. List items (har biri card):
   - **Left:** ikona doiracha (rang: yashil + / qizil -)
   - **Middle:** "Batch bonusi" (title 13px bold) + "24-May, 7:12" (caption 11px muted)
   - **Right:** `+50` yoki `-100` (18px bold, rang)
   - Tap → detail bottom sheet (ixtiyoriy)

**Empty state:**
- 48px icon (💸)
- "Tranzaksiyalar yo'q"
- "Birinchi batch yaratilgach, bu yerda ko'rinadi"

---

### Tab 3: 📦 Batch'lar

**Maqsad:** Do'konga tegishli QR partiyalari + statistika

**Tarkib:**
1. List items (card):
   - Title: "STORE6-MAY-2026-004"
   - 3 ta row: Jami QR, Skanlangan, Aktivatsiya % (rang)
   - **Progress bar** (gradient: ko'k → cyan)
   - Footer: badge (delivery status) + sana + "Batafsil →"
   - Tap → batch detail page (sub-screen)

2. **Batch detail page** (back button bilan):
   - Batch summary card yuqorida
   - "QR kodlar (oxirgi 200 ta)" section title
   - Har QR item:
     - Status dot (yashil = skanlangan, kulrang = yo'q)
     - Serial number (monospace)
     - Agar skanlangan: "👤 Sa'dulla · 24.05.2026 14:22" + "+50"

**Visual idea:** batch card lar **mini-poster** ko'rinishida bo'lsin — yarim shaffof bg pattern, gradient title bar.

---

### Tab 4: 🏆 Top santexniklar

**Maqsad:** Mening do'konimda kim eng faol

**Tarkib:**
1. **Podium top 3** (yuqorida — ixtiyoriy ammo cool)
   - 3-2-1 ranglar (bronze, silver, gold)
   - Har birida avatar/initial circle, ism, ball
2. **List 4–20** — oddiy rank list
   - Rank badge (doiracha, neytral kulrang)
   - Ism + telefon (muted)
   - O'ng tomonda `+N ball` (small label "ball")
   - Skanlar soni "5 ta skan"

**UX:** filter "Bu hafta / Bu oy / Butun davr" (chips)

---

### Tab 5: 🧮 Komissiya kalkulyatori

**Maqsad:** "Agar X dollar sotsam, qancha olaman?"

**Tarkib:**
1. **Info card** — do'kon nomi va komissiya foizi
2. **Big input** — sotuv summasi (USD), katta raqam input
3. **Result card** (yashil gradient): "Sizning komissiyangiz" + `$X.XX` (32px bold)
4. **Disclaimer** (kichik text): "Real summa admin tasdiqlash bilan o'rnatiladi"

**UX:** input real-time recalculate, haptic feedback har 1000 USD qo'shilganda (ixtiyoriy)

---

## 🔧 2-WEBAPP: SANTEXNIK PANELI

**URL:** `/api/webapp/`
**Foydalanuvchi:** Santexnik mutaxassis (oddiy user)
**Tab soni:** 4–5

### Asosiy ekranlar:

#### A. Bosh sahifa (Home)
- **Hero balance card** — gradient (boshqa rang? masalan **purple → pink** sotuvchi'dan farqlash uchun)
- **CTA: "QR kodni skanlash"** — katta tugma, kamera ikona
- **Next gift card** — "Sizga eng yaqin sovg'a"
  - Image + name + progress bar (joriy balans / kerakli)
  - "120 ball qoldi"
- **Quick actions:** Top liderlar | Sovg'alar
- **Promotion banner** — agar joriy akciya bo'lsa

#### B. Sovg'alar (Gifts) — ⭐ ASOSIY EKRAN
**Hozir muammosi:** Card lar bir xil ko'rinadi, qaysisi "men sotib olishim mumkin"ni darrov tushunmaysan.

**Yangi dizayn talab:**
1. **Yuqorida toolbar:**
   - Filter chips: "Hammasi" | "✓ Mavjud" | "⏳ Yaqinda"
   - O'ngda balance pill: "💰 1,250" (joriy)
2. **Grid 2-col mobile:**
   - Card image (1:1 ratio, soft pattern bg)
   - Name (max 2 line)
   - Progress bar — agar < 100% (qanchaga yetdim)
   - Price: `850 ball`
   - **Affordable state:** rangli border + "Olish" CTA mini tugma
   - **Unavailable state:** image 60% opacity + overlay "+200 ball kerak" badge
3. **Tap → bottom sheet detail:**
   - Katta image
   - Toʻliq tavsif
   - Balans status: "Sizda 1,250 / kerak 850" → "+ 400 ball qoladi"
   - CTA "Sovg'a buyurtma qilish" (full width gradient tugma)

#### C. Tarix (History)
- 2 ta sub-tab: "Skanlar" | "Sovg'alar"
- **Skanlar:** har QR kod kartochka — sana, ball, do'kon
- **Sovg'alar:** redemption history — status badge (kutilmoqda / yo'lda / yetkazildi / rad etildi)

#### D. Profil
- Avatar + ism
- Statistika: jami ball, skanlar soni, sovg'alar olingani
- Til tanlash
- Maxfiylik siyosati
- Chiqish

---

## 🎬 Animatsiya va micro-interactions

### Universal qoidalar:
- **Loading:** skeleton shimmer (350ms infinite)
- **Page transition:** fade-in + 8px slide up (300ms ease)
- **Card hover/tap:** scale(0.98) + shadow zo'rayish (150ms)
- **Tab switch:** active dot animation (spring-like)
- **Number changes:** count-up animation (CountUp.js)

### Premium moments:
- **Sovg'a olganda:** confetti + checkmark animation (Lottie)
- **Ball qo'shilganda:** balance card highlight + "+50" floating up
- **Top da rank o'zgarganda:** medal flip

---

## 🌓 Dark mode

Telegram Mini App `var(--tg-theme-*)` auto dark/light qabul qilsin:
- `--tg-theme-bg-color` → body bg
- `--tg-theme-secondary-bg-color` → card bg
- `--tg-theme-text-color` → text
- `--tg-theme-hint-color` → muted

Lekin **gradient hero card lar har doim ko'k qoladi** (brand consistency).

---

## ♿ Accessibility

- **Touch targets:** min 44x44px (Apple guideline)
- **Contrast:** WCAG AA — text vs bg ≥ 4.5:1
- **Font size:** min 12px body text
- **Color blind:** rang + ikona/text (faqat ranga tayanmaslik)
- **Screen reader:** semantic HTML (button vs div onclick=)

---

## 📐 Deliverables (Claude Design dan kutaman)

1. **High-fidelity Figma frames** — har bir ekran uchun (375px va 768px breakpoint)
2. **Design tokens** — CSS variables list (color, spacing, radius, font)
3. **Component library** — button, card, badge, chip, input, tab — har bir variantda
4. **Mini-spec PDF** — har ekran uchun "user story + interaction notes"
5. **Asset export** — SVG icons, logo, illustrations (empty states uchun)
6. **Lottie files** — agar premium animatsiya bo'lsa (sovg'a olish, confetti)
7. **Prototype** — clickable Figma prototype (havola)

---

## ⚠️ Texnik cheklovlar (Claude Design e'tiborga olsin)

- **Vanilla CSS + minimal JS** — React/Vue framework yo'q
- **CDN libraries:** Chart.js bor, Lottie qo'shsa bo'ladi
- **Image size:** logo SVG, gift image lar 200x200 max
- **Performance:** initial paint < 1s, no blocking JS
- **Telegram constraints:**
  - URL bar yo'q (header custom)
  - Back button yo'q (in-app navigation)
  - Notification → Telegram bot orqali (push API yo'q)

---

## 🎨 Mood board references

Claude Design uchun ilhom:
- **Revolut app** — fintech feel, gradient cards
- **N26 Bank** — clean cards, generous spacing
- **Tinkoff** — Russian/CIS market feel
- **Stripe Dashboard** — data viz minimal
- **Linear app** — fast modern feel

**Bizning rejim:** Revolut'ning gradient hero + Linear'ning fast UX + Tinkoff'ning local emotional warmth.

---

## 📋 Implementation handoff (Claude Code → Claude Design)

Design tayyor bo'lgach, men quyidagilarni qilaman:
1. Figma → CSS variables → `core/static/webapp/css/*.css`
2. HTML markup `templates/webapp/{seller,index}.html`
3. JS interactivity vanilla bilan
4. Backend API'lar mavjud (yuqorida endpoints ro'yxati)
5. Telegram WebApp SDK integration: haptic, theme params, init_data auth

**Backend endpoints (tayyor):**
- Sotuvchi: `/api/webapp/seller/{dashboard,transactions,batches,balance-history,batch/<id>/qr,top-santexniks,commission-calc}/`
- Santexnik: `/api/webapp/{user,gifts,redemptions,request-gift,qr-history,promotions,register-qr,...}/`

---

## 📞 Aloqa

- **Loyiha:** JIP Loyalty Platform
- **Loyiha egasi:** Sa'dulla (Bosek)
- **Repository:** GitHub `abbawebuz-agent/abba-ai-bot`, branch `deploy`
- **Production:** https://jip-production.up.railway.app
- **Hozirgi sotuvchi webapp:** `/api/webapp/seller/`
- **Hozirgi santexnik webapp:** `/api/webapp/`

---

**Final deliverable deadline:** Siz aytasiz
**Iterations expected:** 1-2 round of feedback

Rahmat! 🚀
