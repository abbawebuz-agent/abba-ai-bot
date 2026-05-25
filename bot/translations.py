"""
Переводы для Telegram бота на двух языках:
- Узбекский (латиница) - uz_latin
- Русский - ru
"""

from core.dashboard_help import HELP_TEXTS


TRANSLATIONS = {
    'uz_latin': {
        **HELP_TEXTS['uz_latin'],
        'WELCOME': "👋 Xush kelibsiz!\n\nIshni boshlash uchun ro'yxatdan o'tishingiz kerak.\nIltimos, quyidagi tugma orqali telefon raqamingizni yuboring.",
        'ASK_NAME': "👤 Iltimos, ismingizni kiriting:",
        'NAME_SAVED': "✅ Ismingiz saqlandi!",
        'NAME_TOO_SHORT': "❌ Ismingiz juda qisqa. Iltimos, kamida 2 ta belgi kiriting.",
        'SEND_PHONE': "Telefon raqamini yuborish uchun tugmani bosing:",
        'PHONE_SAVED': "✅ Telefon raqamingiz saqlandi!\n\nEndi quyidagi tugma orqali joylashuvingizni yuboring.",
        'SEND_LOCATION': "Joylashuvni yuborish uchun tugmani bosing:",
        'LOCATION_SAVED': "✅ Joylashuvingiz saqlandi!",
        'LOCATION_REQUEST_PROMPT': "📍 Buyurtmalarni yetkazib berish uchun joylashuvingizni ko'rsating.\n\nIltimos, viloyat va tumaningizni tanlang:",
        'LOCATION_CHOOSE_REGION': "Viloyatni tanlang:",
        'LOCATION_CHOOSE_DISTRICT': "Tanlangan viloyat: {region}\n\nTumanni tanlang:",
        'LOCATION_BACK_BUTTON': "« Viloyatlar",
        'LOCATION_SET_SUCCESS': "✅ Joylashuvingiz saqlandi!\n📍 {region}, {district}",
        'REGISTRATION_COMPLETE': "✅ Ro'yxatdan o'tish muvaffaqiyatli yakunlandi!",
        'USE_BUTTON_PHONE': "Iltimos, telefon raqamini yuborish uchun tugmani ishlating.",
        'USE_BUTTON_LOCATION': "Iltimos, joylashuvni yuborish uchun tugmani ishlating.",
        'HINT_USE_BUTTON_BELOW': "Quyidagi tugmani bosing",
        'SELECT_USER_TYPE': "Siz qaysi soha vakilisiz?\n\nAgar siz santexnik (plumber) bo’lsangiz — «Santenik» ni tanlang.\nAgar do’konda sotuvchi yoki do’kon egasi bo’lsangiz — «Sotuvchi» ni tanlang.",
        'USER_TYPE_ELECTRICIAN': "🔧 Santenik",
        'USER_TYPE_SELLER': "🏪 Sotuvchi",
        'USER_TYPE_SAVED': "✅ Kasbingiz saqlandi!",
        'ENTER_SELLER_ID': "🔑 Sotuvchi ID raqamingizni kiriting:\n\n<i>ID raqamini bizdan olgan bo'lishingiz kerak.</i>",
        'SELLER_ID_INVALID': "❌ Noto'g'ri ID. Qaytadan kiriting yoki admin bilan bog'laning: {admin_contact}",
        'SELLER_ID_ALREADY_USED': "⚠️ Bu ID allaqachon ishlatilgan. Admin bilan bog'laning: {admin_contact}",
        'SELLER_ID_ACCEPTED': "✅ ID tasdiqlandi!",
        'SELLER_STORE_NOT_FOUND': "❗ Sizning telefon raqamingiz hech qaysi do'konga biriktirilmagan. Iltimos, admin bilan bog'laning: {admin_contact}",
        'SELLER_STORE_CONFIRM': "🏪 Sizning do'koningiz: <b>{store_name}</b>\n\nManzil: {address}\n\nTo'g'rimi?",
        'SELLER_STORE_CONFIRMED': "✅ Do'konga biriktirildingiz: <b>{store_name}</b>",
        'SELLER_STORE_REJECTED': "❌ Iltimos, admin bilan bog'laning: {admin_contact}",
        # Sotuvchi tasdiqlash tizimi
        'SELLER_PENDING_APPROVAL': (
            "⏳ <b>Arizangiz yuborildi!</b>\n\n"
            "Sizning so'rovingiz admin ko'rib chiqmoqda.\n"
            "Tasdiqlangandan so'ng sizga xabar yuboriladi.\n\n"
            "Savollar uchun: {admin_contact}"
        ),
        'SELLER_APPROVED': (
            "✅ <b>Tabriklaymiz! Arizangiz tasdiqlandi!</b>\n\n"
            "Endi JIP sodiqlik dasturidan foydalanishingiz mumkin.\n"
            "Quyidagi menyudan kerakli bo'limni tanlang."
        ),
        'SELLER_REJECTED': (
            "❌ <b>Arizangiz rad etildi.</b>\n\n"
            "Sabab: {reason}\n\n"
            "Qo'shimcha ma'lumot uchun: {admin_contact}"
        ),
        'SELLER_NOT_APPROVED_YET': (
            "⏳ Arizangiz hali ko'rib chiqilmoqda.\n"
            "Admin tasdiqlashini kuting. Savollar uchun: {admin_contact}"
        ),
        'PRIVACY_POLICY_TEXT': "📄 Iltimos, aksiya shartlari hamda shaxsiy ma’lumotlaringizni qayta ishlash qoidalari bilan tanishing va roziligingizni tasdiqlang.",
        'ACCEPT_PRIVACY': "✅ Shartlar bilan tanishdim va roziman",
        'DECLINE_PRIVACY': "❌ Rad etish",
        'ACCEPT_PRIVACY_QUESTION': "",
        'PRIVACY_ACCEPTED': "✅ Maxfiylik siyosatiga rozilik berildi!",
        'PRIVACY_DECLINED': "❌ Maxfiylik siyosatiga rozilik berilmadi",
        'PRIVACY_REQUIRED': "❌ Ro‘yxatdan o‘tish uchun maxfiylik siyosatiga rozilik berish talab etiladi.",
        'SEND_PHONE_BUTTON': "📱 Telefon raqamini yuborish",
        'REGISTRATION_COMPLETE_MESSAGE': "✅ Ro'yxatdan o'tish muvaffaqiyatli yakunlandi! Endi botdan foydalanishingiz mumkin.",
        'SEND_PROMO_CODE': "Iltimos, o'z promo-kodingizni kiriting.",
        'PROMO_CODE_SAVED': "✅ Promo-kod saqlandi!",
        'ASK_SMARTUP_ID': "SmartUp ID raqamingizni kiriting",
        'SMARTUP_ID_NOT_FOUND': "ID topilmadi. Iltimos, boshqasini sinab ko'ring.",
        
        # QR-код сообщения
        'QR_ACTIVATED': "✅ Promokod muvaffaqiyatli faollashtirildi!\n\n💰 Sizga {points} ball qo'shildi.\n📊 Joriy balansingiz: {total_points} ball.",
        'QR_MAX_ATTEMPTS': "❌ Siz bugun {max_attempts} marta noto'g'ri promokod kiritdingiz.\n\n⏰ Keyingi urinishlar ertaga (00:00) qayta ochiladi.\n\nIltimos, keyinroq urinib ko'ring yoki administrator bilan bog'laning.",
        'QR_NOT_FOUND': "❌ Promokod topilmadi. Kod to'g'riligini tekshiring.",
        'QR_ALREADY_SCANNED': "❌ Bu promokod allaqachon boshqa foydalanuvchi tomonidan ishlatilgan.",
        'QR_WRONG_TYPE': "❌ Promokodlarni faqat santenik kiritishi mumkin. Sotuvchilar balansiga ball admin tomonidan qo'shiladi.",
        'QR_ERROR': "❌ Promokodni qayta ishlashda xatolik yuz berdi. Keyinroq urinib ko'ring.",
        'PROMO_BLOCKED_5_MIN': "❌ Siz 3 marta noto'g'ri promokod kiritdingiz.\n\n⏰ Keyingi urinishlar 5 daqiqadan so'ng ochiladi.",
        'PROMO_BLOCKED_1_DAY': "❌ Siz bir necha marta noto'g'ri promokod kiritdingiz.\n\n⏰ Keyingi urinishlar 24 soatdan so'ng ochiladi.",
        'PROMO_BLOCKED_PERMANENT': "❌ Hisobingiz promokod kiritish uchun bloklandi.\n\nIltimos, administrator bilan bog'laning.",
        
        # Главное меню
        'MAIN_MENU': "👋 Asosiy menyu\n\n💰 Balansingiz: {points} ball\n\nHarakatni tanlang:",
        'MY_GIFTS': "📱 Mening sovg'alarim",
        'OPEN_WEB_APP': "📱 Web ilovani ochish uchun quyidagi tugmani bosing:",
        'GIFTS': "🎁 Sovg'alar",
        'MY_BALANCE': "📊 Mening balansim",
        'TOP_LEADERS': "🏆 TOP yetakchilar",
        'TOP_LEADERS_MONTH': "🏆 TOP (oy)",
        'LANGUAGE': "🌐 Til",
        'ENTER_PROMO_CODE': "🎟 Promokod kiritish",
        
        # Баланс
        'BALANCE_INFO': "💰 Sizning balansingiz: {points} ball",
        
        # Подарки
        'NO_GIFTS': "😔 Hozircha sovg'alar mavjud emas.",
        'GIFTS_LIST': "🎁 Mavjud sovg'alar:\n\n",
        'GIFT_INFO': "{name}\n💎 Narxi: {points_cost} ball\n📝 {description}\n\n",
        'NOT_ENOUGH_POINTS': "❌ Sizda yetarli ball yo'q. Sizga {needed} ball kerak, lekin sizda {have} ball bor.",
        'GIFT_REQUEST_SENT': "✅ Sovg'a olish so'rovingiz '{gift_name}' qabul qilindi!\n\nAdministrator so'rovingizni tez orada ko'rib chiqadi.\n💰 Joriy balansingiz: {remaining_points} ball",
        'GIFT_STATUS_APPROVED': "✅ Tabriklaymiz! Sizning '{gift_name}' sovg'angiz tasdiqlandi!\n\nMahsulot tayyorlash bosqichida.",
        'GIFT_STATUS_SENT': "📦 Sizning '{gift_name}' sovg'angiz yetkazib berish xizmatiga topshirildi!\n\nTez orada sizga yetkaziladi.",
        'GIFT_STATUS_REJECTED': "❌ Afsuski, sizning '{gift_name}' sovg'angiz so'rovi bekor qilindi.\n\nSabab: {admin_notes}\n\nAdministrator bilan bog'laning.",
        'GIFT_STATUS_COMPLETED': "🎉 Tabriklaymiz! Sizning '{gift_name}' sovg'angiz yetkazildi!\n\nMahsulotni qabul qilganingizni tasdiqlang.",
        'INSUFFICIENT_POINTS': "❌ Bu sovg'a uchun yetarli ball yo'q!",
        'GIFT_NOT_FOUND': "❌ Sovg'a topilmadi!",
        'GIFT_NOT_AVAILABLE_FOR_USER_TYPE': "❌ Bu sovg'a sizning foydalanuvchi turingiz uchun mavjud emas!",
        'GIFT_REQUEST_ERROR': "❌ Xatolik yuz berdi. Keyinroq urinib ko'ring.",
        
        # ТОП лидеры
        'TOP_LEADERS_TITLE': "🏆 TOP 10 yetakchilar:\n\n",
        'TOP_LEADERS_MONTH_TITLE': "🏆 TOP 10 (joriy oy):\n\n",
        'LEADER_ENTRY': "{position}. {name} - {points} ball\n",
        'NO_LEADERS': "😔 Hozircha yetakchilar yo'q.",
        'NO_LEADERS_MONTH': "😔 Joriy oy uchun yetakchilar yo'q.",
        'USER': "Foydalanuvchi",
        
        # Смена языка
        'SELECT_LANGUAGE': "🌐 Tilni tanlang:",
        'LANGUAGE_CHANGED': "✅ Til o'zgartirildi!",
        'UZBEK_LATIN': "🇺🇿 O'zbek (Lotin)",
        'RUSSIAN': "🇷🇺 Русский",
        'VIDEO_INSTRUCTION_CAPTION': "Botning funksiyalarini o'rganish va undan to'g'ri foydalanishni o'rganish uchun video qo'llanmani ko'ring.",
        
        # Ошибки
        'ERROR_OCCURRED': "❌ Xatolik yuz berdi. Iltimos, keyinroq urinib ko'ring.",
        'UNKNOWN_COMMAND': "Men bu buyruqni tushunmayapman. Menyu tugmalaridan foydalaning.",
        'PLEASE_START': "👋 Botdan foydalanish uchun avval ro'yxatdan o'ting.\n\nIltimos, /start buyrug'ini yuboring.",
        
        # Web App переводы
        'WEBAPP_MY_GIFTS': "Mening sovg’alarim",
        'WEBAPP_YOUR_POINTS': "Sizning ballingiz",
        'WEBAPP_TOTAL_POINTS': "Jami ballar",
        'WEBAPP_AVAILABLE_GIFTS': "🎁 Mavjud sovg’alar",
        'WEBAPP_MY_ORDERS': "📦 Mening buyurtmalarim",
        'WEBAPP_LOADING': "Yuklanmoqda...",
        'WEBAPP_LOADING_GIFTS': "Sovg’alar yuklanmoqda...",
        'WEBAPP_LOADING_ORDERS': "Buyurtmalar yuklanmoqda...",
        'WEBAPP_NO_GIFTS': "Mavjud sovg’alar yo’q",
        'WEBAPP_NO_ORDERS': "Sizda hozircha buyurtmalar yo'q",
        'WEBAPP_NO_ORDERS_TEXT': "Bu yerda siz buyurtma qilgan sovg'alar ko'rsatiladi. Birinchi sovg'angizni buyurtma qilganingizdan keyin, u shu bo'limda paydo bo'ladi.",
        'WEBAPP_POINTS': "ball",
        'WEBAPP_CONFIRM_RECEIPT': "Qabul qilishni tasdiqlash",
        'WEBAPP_DID_YOU_RECEIVE': "Siz buyurtmani oldingizmi?",
        'WEBAPP_COMMENT_PLACEHOLDER': "Agar olmagan bo’lsangiz, sababni va qo’ng’iroq qilish so’rovingizni ko’rsating...",
        'WEBAPP_YES_RECEIVED': "Ha, oldim",
        'WEBAPP_NO_NOT_RECEIVED': "Yo’q, olmadim",
        'WEBAPP_CANCEL': "Bekor qilish",
        'WEBAPP_CONFIRM_REQUEST': "Siz bu sovg’ani so’rashni xohlaysizmi?",
        'WEBAPP_REQUEST_SENT': "Sovg’a sorish so’rovi yuborildi!",
        'WEBAPP_ERROR': "Xatolik: {error}",
        'WEBAPP_ERROR_LOADING_USER': "Foydalanuvchi ma’lumotlarini yuklab bo’lmadi",
        'WEBAPP_ERROR_LOADING_GIFTS': "Sovg’alarni yuklashda xatolik",
        'WEBAPP_ERROR_LOADING_ORDERS': "Buyurtmalarni yuklashda xatolik",
        'WEBAPP_ERROR_REQUESTING_GIFT': "Sovg’a so’rashda xatolik",
        'WEBAPP_ERROR_CONFIRMING': "Tasdiqlashda xatolik",
        'WEBAPP_THANKS_CONFIRMATION': "Tasdiqlash uchun rahmat!",
        'WEBAPP_COMMENT_SENT': "Sizning izohingiz yuborildi. Siz bilan bog’lanamiz.",
        'WEBAPP_COMMENT_REQUIRED': "Iltimos, buyurtmani olmagan sababingizni ko’rsating",
        'WEBAPP_STATUS_PENDING': "Kutish jarayonida",
        'WEBAPP_STATUS_APPROVED': "Mahsulot tayyorlash bosqichida",
        'WEBAPP_STATUS_SENT': "Mahsulot yetkazib berish xizmatiga topshirildi",
        'WEBAPP_STATUS_REJECTED': "So'rov bekor qilindi (administrator bilan bog'lanamiz)",
        'WEBAPP_STATUS_COMPLETED': "Mahsulotni qabul qilganingizni tasdiqlang",
        'WEBAPP_STATUS_RECEIVED': "Qabul qilingan mahsulot",
        'WEBAPP_STATUS_NOT_RECEIVED': "Sovg'a berilmagan",
        'WEBAPP_STATUS_CANCELLED_BY_USER': "Foydalanuvchi tomonidan bekor qilindi",
        'WEBAPP_CANCEL_ORDER': "Buyurtmani bekor qilish",
        'WEBAPP_CANCEL_ORDER_CONFIRM': "Buyurtmani bekor qilishni xohlaysizmi? Ballar qaytariladi.",
        'WEBAPP_CANCEL_ORDER_SUCCESS': "Buyurtma bekor qilindi. Ballar qaytarildi.",
        'WEBAPP_CANCEL_ORDER_EXPIRED': "Bekor qilish muddati o'tgan (1 soat).",
        'WEBAPP_DELIVERY_PENDING': "Yuborish kutilmoqda",
        'WEBAPP_DELIVERY_SENT': "Yuborildi",
        'WEBAPP_DELIVERY_DELIVERED': "Yetkazildi",
        'WEBAPP_DELIVERY_STATUS': "Yetkazib berish holati:",
        'WEBAPP_REQUESTED': "So’ralgan:",
        'WEBAPP_YOUR_COMMENT': "Sizning izohingiz:",
        'WEBAPP_CONFIRM_RECEIPT_BUTTON': "Qabul qilishni tasdiqlash",
        'WEBAPP_BACK': "Orqaga",
        'WEBAPP_PARTNER_TEXT': "JIP bilan hamkorlik qilib va sovg’alarga erishing",
        'WEBAPP_CONTACT_ADMIN': "Admin bilan bog’laning",
        'WEBAPP_INFO_TEXT': "Ballar promokodni skanerdan oʻtkazganingizdan soʻng darhol hisobingizga tushadi. Agar ballar tushmagan boʻlsa, iltimos, administratorga murojaat qiling.",
        'WEBAPP_REGISTER': "Ro’yxatdan o’tkazish",
        'WEBAPP_VIEW_GIFTS': "Sovg’alarni ko’rish",
        'WEBAPP_PRIVACY_POLICY': "Maxfiylik siyosati",
        'WEBAPP_QR_CODE_ERROR': "Noto’g’ri kod kiritildi",
        'WEBAPP_PROMO_CODE_ERROR': "Noto’g’ri promokod kiritildi",
        'WEBAPP_QR_PLACEHOLDER': "Promokodni kiriting",
        'WEBAPP_GIFTS_TITLE': "Sovg’alar",
        'WEBAPP_GIFT_NAME': "Sovg’a nomi",
        'WEBAPP_GET_GIFT': "Sovg’ani olish",
        'WEBAPP_NOT_ENOUGH_POINTS': "Ballar yetarli emas",
        'WEBAPP_WAITING_PROCESS': "Kutish jarayonida",
        'WEBAPP_SUCCESS_TITLE': "Muvaffaqiyatli bajarildi!",
        'WEBAPP_SUCCESS_MESSAGE': "Sizning sovg’angiz tayyorlanmoqda, yaqin orada bizning xodimlarimiz siz bilan bog’lanadi.",
        'WEBAPP_TO_HOME': "Bosh sahifaga",
        'WEBAPP_GIFT_IN_STOCK': "Mavjud",
        'WEBAPP_GIFT_COST': "Narxi",
        'WEBAPP_GIFT_AFTER_REDEMPTION': "Olishdan keyin",
        'WEBAPP_CONTACT_ADMIN_CHOOSE': "Qulay aloqa usulini tanlang",
        'WEBAPP_PROFILE': "Profil",
        'WEBAPP_INTERFACE_LANGUAGE': "Interfeys tili",
        'WEBAPP_GIFTS': "Mening sovg’alarim",
        'WEBAPP_QR_HISTORY': "Promokodlar tarixi",
        'WEBAPP_NAV_HOME': "Bosh sahifa",
        'WEBAPP_NAV_GIFTS': "Sovg’alar",
        'WEBAPP_NAV_HISTORY': "Promokodlar",
        'WEBAPP_NAV_MY_GIFTS': "Mening sovg’alarim",
        'WEBAPP_NAV_PROFILE': "Profil",
        'WEBAPP_USER_TYPE_ELECTRICIAN': "Santenik",
        'WEBAPP_USER_TYPE_SELLER': "Sotuvchi",
        'WEBAPP_MY_GIFTS_MENU': "Mening sovg’alarim",
        'WEBAPP_LIVE_STREAMS_TITLE': "Jonli efirlar",
        'WEBAPP_LIVE_STREAMS_UPCOMING': "Yaqinlashayotgan efirlar",
        'WEBAPP_LIVE_STREAMS_PAST': "O‘tgan efirlar",
        'WEBAPP_LIVE_STREAM_OPEN': "Efirni ochish",
        'WEBAPP_LIVE_STREAM_WATCH_RECORDING': "Yozuvni ko‘rish",
        'WEBAPP_LIVE_STREAM_NO_UPCOMING': "Yaqinlashayotgan efirlar yo‘q",
        'WEBAPP_LIVE_STREAM_NO_PAST': "O‘tgan efirlar yo‘q",
        'WEBAPP_LIVE_STREAM_WINNERS_ELECTRICIANS': "G‘oliblar — santexniklar",
        'WEBAPP_LIVE_STREAM_WINNERS_SELLERS': "G‘oliblar — tadbirkorlar",
        'WEBAPP_LIVE_STREAM_NO_WINNERS': "G‘oliblar hali e’lon qilinmagan",
        'WEBAPP_LIVE_STREAM_LOADING': "Jonli efirlar yuklanmoqda...",
        'WEBAPP_MONTHLY_CHANCES': "{count} ta shans",
        'WEBAPP_QR_FILTER_CURRENT_MONTH': "Bu oy",
        'WEBAPP_QR_FILTER_ALL': "Hammasi",
        'WEBAPP_TICKET_NUMBER': "Bilet №{order}",
        'WEBAPP_TICKET_NUMBER_SHORT': "№",
        'WEBAPP_TICKET_LABEL': "BILET",
        'WEBAPP_RAFFLE_TICKETS': "Lotereya promokodlari",
        'WEBAPP_RAFFLE_FINISHED': "lotereya yakunlandi",
        'WEBAPP_CHANCES': "shans",
        'WEBAPP_QR_CURRENT_MONTH_TITLE': "lotereya promokodlari",
        'WEBAPP_QR_ARCHIVE': "arxiv",
        'WEBAPP_BALL_SHORT': "b",
        'WEBAPP_OPEN': "Ochish",
        'WEBAPP_PLAY': "Ijro",
        'WEBAPP_PLACE': "O'rin",
        'WEBAPP_LIVE_RECORD': "● YOZUV",
        'WEBAPP_LIVE_PARTICIPANTS': "Ishtirokchilar",
        'WEBAPP_LIVE_WINNERS': "G‘oliblar",
        'WEBAPP_LIVE_WINNERS_TITLE': "Efir — g‘oliblar",
        'WEBAPP_LIVE_FOOTNOTE': "G‘oliblar tasodifiy tanlangan",
        'WEBAPP_TAB_ELECTRICIANS': "Santexniklar",
        'WEBAPP_TAB_SELLERS': "Sotuvchilar",
        'WEBAPP_PRIZE': "Sovg‘a",
        'WEBAPP_TOP_USERS_TITLE_ELECTRICIANS': "Top santexniklar",
        'WEBAPP_TOP_USERS_TITLE_SELLERS': "Top tadbirkorlar",
        'WEBAPP_TOP_USERS_PERIOD_ALL': "Butun davr uchun",
        'WEBAPP_TOP_USERS_PERIOD_CURRENT': "Joriy oy",
        'WEBAPP_TOP_USERS_EMPTY': "Ma’lumot yo‘q",
        'WEBAPP_TOP_USERS_YOU': "Siz",
        'WEBAPP_TOP_USERS_NOT_RANKED': "—",
        'WEBAPP_TOP_USERS_POINTS_SHORT': "ball",
        'MONTHLY_CHANCES_LINE': "Bu oydagi shanslaringiz: {count}",
        'WEBAPP_UZBEK': "O’zbekcha",
        'WEBAPP_RUSSIAN': "Ruscha",
        'WEBAPP_UPDATED': "Yangilangan",
        'WEBAPP_CLOSE': "Yopish",
        'WEBAPP_BALL': "Ball",
        'WEBAPP_NEXT_GIFT_LABEL': "Keyingi sovg’a:",
        'WEBAPP_POINTS_NEEDED_MORE': "Sizga yana {points} ball kerak",
        'WEBAPP_ORDERS_TITLE': "Mening buyurtmalarim",
        'WEBAPP_ORDERS_TOTAL': "{count} ta jami",
        'WEBAPP_ORDERS_TAB_ACTIVE': "Faol",
        'WEBAPP_ORDERS_TAB_DELIVERED': "Yetkazilgan",
        'WEBAPP_ORDER_NUMBER': "Buyurtma #{n}",
        'WEBAPP_STEP_CONFIRMED': "Tasdiqlandi",
        'WEBAPP_STEP_SHIPPED': "Yo‘lda",
        'WEBAPP_STEP_DELIVERED': "Yetkazildi",
        'WEBAPP_BADGE_PROCESSING': "Kutilmoqda",
        'WEBAPP_BADGE_CONFIRMED': "Tasdiqlandi",
        'WEBAPP_BADGE_ON_THE_WAY': "Yo‘lda",
        'WEBAPP_BADGE_DELIVERED': "Yetkazildi",
        'WEBAPP_BADGE_RECEIVED': "Qabul qilindi",
        'WEBAPP_BADGE_REJECTED': "Bekor qilindi",
        'WEBAPP_BADGE_CANCELLED': "Bekor qildingiz",
        'WEBAPP_BADGE_NOT_RECEIVED': "Olinmadi",
        'WEBAPP_ORDERS_EMPTY_TAB': "Bu bo‘limda buyurtmalar yo‘q",
        'WEBAPP_LOADING_QR_HISTORY': "Promokodlar tarixi yuklanmoqda...",
        'WEBAPP_NO_QR_HISTORY': "Promokodlar tarixi yo’q",
        'WEBAPP_QR_MAX_ATTEMPTS': "❌ Siz bugun {max_attempts} marta noto’g’ri promokod kiritdingiz. Keyingi urinishlar ertaga (00:00) qayta ochiladi.",
        'WEBAPP_QR_WRONG_TYPE': "❌ Bu promokod sizning turingizga mos kelmaydi. Siz faqat o’z turingizga mos promokodlarni kiritishingiz mumkin.",
        'WEBAPP_PRIVACY_PDF_DESCRIPTION': "Maxfiylik siyosati PDF formatida mavjud. Hujjatni ochish uchun quyidagi tugmani bosing.",
        'WEBAPP_OPEN_PDF': "PDF-ni ochish",

        # Dashboard UI (Exact from ui_translations_exact_uz.json)
        'DASHBOARD_USER_OVERVIEW': "Foydalanuvchilar soni",
        'DASHBOARD_ELECTRICIAN_CODES': "Santenik kodlari soni",
        'DASHBOARD_STORE_CODES': "Do'kon kodlari",
        'DASHBOARD_TOTAL_POINTS': "Ballar miqdori",
        'DASHBOARD_ELECTRICIAN_POOL': "Santenik ballari miqdori",
        'DASHBOARD_STORE_POOL': "Do'kon ballari miqdori",
        'DASHBOARD_GIFT_REQUESTS': "Sovg'alar soni",
        'DASHBOARD_GIFTS_ELECTRICIANS': "Sovg'alar — Santenik",
        'DASHBOARD_GIFTS_STORES': "Sovg'alar — Do'konlar",

        'DASHBOARD_TAB_GENERAL': "Umumiy",
        'DASHBOARD_TAB_STORES': "Aksiyada ishtirok etayotgan do'konlar",
        'DASHBOARD_TAB_ELECTRICIANS': "Aksiyada ishtirok etayotgan santenik",

        'DASHBOARD_FILTER_PERIOD': "Davr:",
        'DASHBOARD_FILTER_FROM': "Dan",
        'DASHBOARD_FILTER_TO': "Gacha",
        'DASHBOARD_FILTER_APPLY': "Qo'llash",
        'DASHBOARD_FILTER_RESET': "Tozalash",
        'DASHBOARD_FILTER_ALL_TIME': "Butun davr",

        'DASHBOARD_LABEL_ELECTRICIANS': "Santenik",
        'DASHBOARD_LABEL_STORES': "Do'konlar",
        'DASHBOARD_LABEL_UNSELECTED': "Tanlanmagan",
        'DASHBOARD_LABEL_SCANNED': "Skanerlangan",
        'DASHBOARD_LABEL_SCANNED_TOTAL': "Umumiy skanerlangan",
        'DASHBOARD_LABEL_SCANNED_PERIOD': "Davr mobaynida skanerlangan",
        'DASHBOARD_LABEL_SPENT': "Sarflangan",
        'DASHBOARD_LABEL_REMAINING': "Skanerlanmagan",

        'DASHBOARD_LABEL_SCANNED_TOTAL_COUNT': "Umumiy skanerlangan (soni)",
        'DASHBOARD_LABEL_SCANNED_PERIOD_COUNT': "Davr mobaynida skanerlangan (soni)",
        'DASHBOARD_LABEL_REMAINING_COUNT': "Skanerlanmagan (soni)",

        'DASHBOARD_LABEL_SCANNED_TOTAL_POINTS': "Umumiy skanerlangan (ball)",
        'DASHBOARD_LABEL_SCANNED_PERIOD_POINTS': "Davr mobaynida skanerlangan (ball)",
        'DASHBOARD_LABEL_SPENT_POINTS': "Sarflangan (ball)",
        'DASHBOARD_LABEL_REMAINING_POINTS': "Skanerlanmagan (ball)",

        'NEW_THIS_PERIOD': "Davr mobaynida yangi",

        'DASHBOARD_STATUS_SUCCESS': "Topshirilgan",
        'DASHBOARD_STATUS_PENDING': "Jarayonda",
        'DASHBOARD_STATUS_REJECTED': "Topshirilmagan",

        'DASHBOARD_STATUS': "Holati",
        'DASHBOARD_HEADER_COUNT': "Sonda",
        'DASHBOARD_HEADER_POINTS': "Ballda",
        'DASHBOARD_TOTAL': "Jami",

        'DASHBOARD_CHART_POPULAR_GIFTS': "Eng ommabop sovg'alar",
        'DASHBOARD_CHART_REQUEST_STATUSES': "So'rovlar holati",
        'DASHBOARD_CHART_DISTRICT_DISTRIBUTION': "Tuman kesimidagi statistika",
        'DASHBOARD_CHART_REGIONAL_DISTRIBUTION': "Viloyatlar kesimidagi statistika",

        # Sotuvchi asosiy menyusi
        'SELLER_MAIN_MENU': "👋 Assalomu alaykum, {name}!\n\n🏪 Do'kon: {store}\n💰 Balansingiz: {points} ball\n\nHarakatni tanlang:",
        'SELLER_MY_BALANCE': "💰 Mening balansim",
        'SELLER_SALES_HISTORY': "📊 Sotuv tarixi",
        'SELLER_MY_STORE': "🏪 Mening do'konim",
        'SELLER_OPEN_WEBAPP': "🌐 Web ilovani ochish",
        'SELLER_CONTACT_ADMIN': "📞 Admin bilan bog'lanish",
        'SELLER_BALANCE_INFO': "💰 Sizning balansingiz: {points} ball\n\nBallar faqat admin tomonidan qo'shiladi.",
        'SELLER_STORE_INFO': "🏪 <b>{name}</b>\n\n📍 Manzil: {address}\n📊 Viloyat: {region}\n\n📦 Kartalar: {total} ta (skanlangan: {scanned})\n💳 Komissiya: {commission}%",
        'SELLER_NO_STORE': "❗ Sizning do'koningiz topilmadi. Admin bilan bog'laning.",
        'SELLER_WEBAPP_BUTTON': "📊 Sotuvchi paneli",
        'SELLER_REG_SUCCESS': (
            "✅ <b>Ro'yxatdan muvaffaqiyatli o'tdingiz!</b>\n\n"
            "Endi sotuvchi panelidan foydalanishingiz mumkin. "
            "Quyidagi tugmani bosing va Web App ochiladi."
        ),
    },

    'ru': {
        **HELP_TEXTS['ru'],
        # Основные сообщения
        'WELCOME': "👋 Добро пожаловать!\n\nДля начала работы необходимо пройти регистрацию.\nПожалуйста, отправьте ваш номер телефона, используя кнопку ниже.",
        'ASK_NAME': "👤 Пожалуйста, введите ваше имя:",
        'NAME_SAVED': "✅ Имя сохранено!",
        'NAME_TOO_SHORT': "❌ Имя слишком короткое. Пожалуйста, введите минимум 2 символа.",
        'SEND_PHONE': "Нажмите на кнопку, чтобы отправить номер телефона:",
        'PHONE_SAVED': "✅ Номер телефона сохранен!\n\nТеперь отправьте вашу локацию, используя кнопку ниже.",
        'SEND_LOCATION': "Нажмите на кнопку, чтобы отправить локацию:",
        'LOCATION_SAVED': "✅ Локация сохранена!",
        'LOCATION_REQUEST_PROMPT': "📍 Чтобы мы могли доставить ваши заказы, укажите вашу локацию.\n\nПожалуйста, выберите регион и район:",
        'LOCATION_CHOOSE_REGION': "Выберите регион:",
        'LOCATION_CHOOSE_DISTRICT': "Выбранный регион: {region}\n\nВыберите район:",
        'LOCATION_BACK_BUTTON': "« К регионам",
        'LOCATION_SET_SUCCESS': "✅ Локация сохранена!\n📍 {region}, {district}",
        'REGISTRATION_COMPLETE': "✅ Регистрация завершена!",
        'USE_BUTTON_PHONE': "Пожалуйста, используйте кнопку для отправки номера телефона.",
        'USE_BUTTON_LOCATION': "Пожалуйста, используйте кнопку для отправки геолокации.",
        'HINT_USE_BUTTON_BELOW': "Используйте кнопку ниже",
        'SELECT_USER_TYPE': "К какой категории вы относитесь?\n\nЕсли вы сантехник (plumber) — выберите «Сантеник».\nЕсли вы продавец или владелец магазина — выберите «Продавец».",
        'USER_TYPE_ELECTRICIAN': "🔧 Сантеник",
        'USER_TYPE_SELLER': "🏪 Продавец",
        'USER_TYPE_SAVED': "✅ Тип сохранен!",
        'ENTER_SELLER_ID': "🔑 Введите ваш ID продавца:\n\n<i>ID должен быть получен от нас.</i>",
        'SELLER_ID_INVALID': "❌ Неверный ID. Попробуйте ещё раз или свяжитесь с администратором: {admin_contact}",
        'SELLER_ID_ALREADY_USED': "⚠️ Этот ID уже использован. Свяжитесь с администратором: {admin_contact}",
        'SELLER_ID_ACCEPTED': "✅ ID подтверждён!",
        'PRIVACY_POLICY_TEXT': "📄 Пожалуйста, ознакомьтесь с условиями участия в программе и правилами обработки ваших персональных данных, затем подтвердите свое согласие.",
        'ACCEPT_PRIVACY': "✅  Ознакомился с условиями и даю своё согласие",
        'DECLINE_PRIVACY': "❌ Отклонить",
        'ACCEPT_PRIVACY_QUESTION': "",
        'PRIVACY_ACCEPTED': "✅ Согласие на политику конфиденциальности получено!",
        'PRIVACY_DECLINED': "❌ Согласие на политику конфиденциальности не получено",
        'PRIVACY_REQUIRED': "❌ Для регистрации необходимо согласие с политикой конфиденциальности.",
        'SELLER_STORE_NOT_FOUND': "❗ Ваш номер телефона не привязан ни к одному магазину. Пожалуйста, свяжитесь с администратором: {admin_contact}",
        'SELLER_STORE_CONFIRM': "🏪 Ваш магазин: <b>{store_name}</b>\n\nАдрес: {address}\n\nВерно?",
        'SELLER_STORE_CONFIRMED': "✅ Вы привязаны к магазину: <b>{store_name}</b>",
        'SELLER_STORE_REJECTED': "❌ Пожалуйста, свяжитесь с администратором: {admin_contact}",
        # Sotuvchi tasdiqlash tizimi
        'SELLER_PENDING_APPROVAL': (
            "⏳ <b>Ваша заявка отправлена!</b>\n\n"
            "Администратор рассматривает вашу заявку.\n"
            "После одобрения вам придёт уведомление.\n\n"
            "По вопросам: {admin_contact}"
        ),
        'SELLER_APPROVED': (
            "✅ <b>Поздравляем! Ваша заявка одобрена!</b>\n\n"
            "Теперь вы можете пользоваться программой лояльности JIP.\n"
            "Выберите нужный раздел в меню."
        ),
        'SELLER_REJECTED': (
            "❌ <b>Ваша заявка отклонена.</b>\n\n"
            "Причина: {reason}\n\n"
            "По вопросам: {admin_contact}"
        ),
        'SELLER_NOT_APPROVED_YET': (
            "⏳ Ваша заявка ещё рассматривается.\n"
            "Ожидайте одобрения администратора. По вопросам: {admin_contact}"
        ),
        'SEND_PHONE_BUTTON': "📱 Отправить номер телефона",
        'REGISTRATION_COMPLETE_MESSAGE': "✅ Регистрация успешно завершена! Теперь вы можете пользоваться ботом.",
        'SEND_PROMO_CODE': "Пожалуйста, введите ваш промокод.",
        'PROMO_CODE_SAVED': "✅ Промокод сохранен!",
        'ASK_SMARTUP_ID': "Введите ID вашего SmartUp",
        'SMARTUP_ID_NOT_FOUND': "ID не найден. Пожалуйста, попробуйте другой.",
        
        # QR-код сообщения
        'QR_ACTIVATED': "✅ Промокод успешно активирован!\n\n💰 Вам начислено {points} баллов.\n📊 Ваш текущий баланс: {total_points} баллов.",
        'QR_MAX_ATTEMPTS': "❌ Вы сегодня {max_attempts} раз ввели неверный Promokod.\n\n⏰ Следующие попытки откроются завтра (00:00).\n\nПожалуйста, попробуйте позже или свяжитесь с администратором.",
        'QR_NOT_FOUND': "❌ Промокод не найден. Проверьте правильность кода.",
        'QR_ALREADY_SCANNED': "❌ Этот Промокод уже был использован другим пользователем.",
        'QR_WRONG_TYPE': "❌ Промокоды может вводить только сантеник. Баллы продавца начисляются администратором вручную.",
        'QR_ERROR': "❌ Произошла ошибка при обработке Промокода. Попробуйте позже.",
        'PROMO_BLOCKED_5_MIN': "❌ Вы 3 раза подряд ввели неверный промокод.\n\n⏰ Следующие попытки будут доступны через 5 минут.",
        'PROMO_BLOCKED_1_DAY': "❌ Вы многократно вводили неверные промокоды.\n\n⏰ Следующие попытки будут доступны через 24 часа.",
        'PROMO_BLOCKED_PERMANENT': "❌ Ваш аккаунт заблокирован для ввода промокодов.\n\nПожалуйста, свяжитесь с администратором.",
        
        # Главное меню
        'MAIN_MENU': "👋 Главное меню\n\n💰 Ваш баланс: {points} баллов\n\nВыберите действие:",
        'MY_GIFTS': "📱 Мои подарки",
        'OPEN_WEB_APP': "📱 Нажмите кнопку ниже, чтобы открыть веб-приложение:",
        'GIFTS': "🎁 Подарки",
        'MY_BALANCE': "📊 Мой баланс",
        'TOP_LEADERS': "🏆 ТОП лидеры",
        'TOP_LEADERS_MONTH': "🏆 ТОП (месяц)",
        'LANGUAGE': "🌐 Язык",
        'ENTER_PROMO_CODE': "🎟 Ввести промокод",
        
        # Баланс
        'BALANCE_INFO': "💰 Ваш текущий баланс: {points} баллов",
        
        # Подарки
        'NO_GIFTS': "😔 К сожалению, сейчас нет доступных подарков.",
        'GIFTS_LIST': "🎁 Доступные подарки:\n\n",
        'GIFT_INFO': "{name}\n💎 Стоимость: {points_cost} баллов\n📝 {description}\n\n",
        'NOT_ENOUGH_POINTS': "❌ Недостаточно баллов. Вам нужно {needed} баллов, но у вас {have} баллов.",
        'GIFT_REQUEST_SENT': "✅ Ваш запрос на получение подарка '{gift_name}' принят!\n\nАдминистратор обработает ваш запрос в ближайшее время.\n💰 Ваш текущий баланс: {remaining_points} баллов",
        'GIFT_STATUS_APPROVED': "✅ Поздравляем! Ваш запрос на подарок '{gift_name}' одобрен!\n\nПродукт находится в стадии подготовки.",
        'GIFT_STATUS_SENT': "📦 Ваш подарок '{gift_name}' передан в службу доставки!\n\nСкоро он будет доставлен вам.",
        'GIFT_STATUS_REJECTED': "❌ К сожалению, ваш запрос на подарок '{gift_name}' отменен.\n\n{admin_notes}\n\nСвяжитесь с администратором.",
        'GIFT_STATUS_COMPLETED': "🎉 Поздравляем! Ваш подарок '{gift_name}' доставлен!\n\nПодтверждение получения продукта.",
        'INSUFFICIENT_POINTS': "❌ Недостаточно баллов для этого подарка!",
        'GIFT_NOT_FOUND': "❌ Подарок не найден!",
        'GIFT_NOT_AVAILABLE_FOR_USER_TYPE': "❌ Этот подарок недоступен для вашего типа пользователя!",
        'GIFT_REQUEST_ERROR': "❌ Произошла ошибка. Попробуйте позже.",
        
        # ТОП лидеры
        'TOP_LEADERS_TITLE': "🏆 ТОП-10 лидеров:\n\n",
        'TOP_LEADERS_MONTH_TITLE': "🏆 ТОП-10 (текущий месяц):\n\n",
        'LEADER_ENTRY': "{position}. {name} - {points} баллов\n",
        'NO_LEADERS': "😔 Пока нет лидеров.",
        'NO_LEADERS_MONTH': "😔 За текущий месяц лидеров пока нет.",
        'USER': "Пользователь",
        
        # Смена языка
        'SELECT_LANGUAGE': "🌐 Выберите язык:",
        'LANGUAGE_CHANGED': "✅ Язык изменен!",
        'UZBEK_LATIN': "🇺🇿 O'zbek (Lotin)",
        'RUSSIAN': "🇷🇺 Русский",
        'VIDEO_INSTRUCTION_CAPTION': "Просмотрите видеоинструкцию, чтобы ознакомиться с функционалом бота и научиться им пользоваться",
        
        # Ошибки
        'ERROR_OCCURRED': "❌ Произошла ошибка. Попробуйте позже.",
        'UNKNOWN_COMMAND': "Я не понимаю эту команду. Используйте кнопки меню.",
        'PLEASE_START': "👋 Чтобы пользоваться ботом, сначала зарегистрируйтесь.\n\nОтправьте команду /start",
        
        # Web App переводы
        'WEBAPP_MY_GIFTS': "Мои подарки",
        'WEBAPP_YOUR_POINTS': "Ваши баллы",
        'WEBAPP_TOTAL_POINTS': "Всего баллов",
        'WEBAPP_AVAILABLE_GIFTS': "🎁 Доступные подарки",
        'WEBAPP_MY_ORDERS': "📦 Мои заказы",
        'WEBAPP_LOADING': "Загрузка...",
        'WEBAPP_LOADING_GIFTS': "Загрузка подарков...",
        'WEBAPP_LOADING_ORDERS': "Загрузка заказов...",
        'WEBAPP_NO_GIFTS': "Нет доступных подарков",
        'WEBAPP_NO_ORDERS': "У вас пока нет заказанных призов",
        'WEBAPP_NO_ORDERS_TEXT': "Здесь будут отображаться призы, которые вы закажете. Как только вы оформите первый приз, он появится в этом разделе.",
        'WEBAPP_POINTS': "баллов",
        'WEBAPP_CONFIRM_RECEIPT': "Подтверждение получения",
        'WEBAPP_DID_YOU_RECEIVE': "Вы получили заказ?",
        'WEBAPP_COMMENT_PLACEHOLDER': "Если не получили, укажите причину и просьбу позвонить...",
        'WEBAPP_YES_RECEIVED': "Да, получил",
        'WEBAPP_NO_NOT_RECEIVED': "Нет, не получил",
        'WEBAPP_CANCEL': "Отмена",
        'WEBAPP_CONFIRM_REQUEST': "Вы уверены, что хотите запросить этот подарок?",
        'WEBAPP_REQUEST_SENT': "Запрос на получение подарка отправлен!",
        'WEBAPP_ERROR': "Ошибка: {error}",
        'WEBAPP_ERROR_LOADING_USER': "Не удалось получить данные пользователя",
        'WEBAPP_ERROR_LOADING_GIFTS': "Ошибка загрузки подарков",
        'WEBAPP_ERROR_LOADING_ORDERS': "Ошибка загрузки заказов",
        'WEBAPP_ERROR_REQUESTING_GIFT': "Ошибка при запросе подарка",
        'WEBAPP_ERROR_CONFIRMING': "Ошибка при подтверждении",
        'WEBAPP_THANKS_CONFIRMATION': "Спасибо за подтверждение!",
        'WEBAPP_COMMENT_SENT': "Ваш комментарий отправлен. С вами свяжутся.",
        'WEBAPP_COMMENT_REQUIRED': "Пожалуйста, укажите причину, почему вы не получили заказ",
        'WEBAPP_STATUS_PENDING': "Запрос принят к обработке",
        'WEBAPP_STATUS_APPROVED': "Продукт находится в стадии подготовки",
        'WEBAPP_STATUS_SENT': "Продукт передан в службу доставки",
        'WEBAPP_STATUS_REJECTED': "Запрос отменен (свяжитесь с администратором)",
        'WEBAPP_STATUS_COMPLETED': "Подтверждение получения продукта",
        'WEBAPP_STATUS_RECEIVED': "Полученный товар",
        'WEBAPP_STATUS_NOT_RECEIVED': "Подарок не выдан",
        'WEBAPP_STATUS_CANCELLED_BY_USER': "Отменено пользователем",
        'WEBAPP_CANCEL_ORDER': "Отменить заказ",
        'WEBAPP_CANCEL_ORDER_CONFIRM': "Вы уверены, что хотите отменить заказ? Баллы будут возвращены.",
        'WEBAPP_CANCEL_ORDER_SUCCESS': "Заказ отменен. Баллы возвращены.",
        'WEBAPP_CANCEL_ORDER_EXPIRED': "Время для отмены истекло (1 час).",
        'WEBAPP_DELIVERY_PENDING': "Ожидает отправки",
        'WEBAPP_DELIVERY_SENT': "Отправлено",
        'WEBAPP_DELIVERY_DELIVERED': "Доставлено",
        'WEBAPP_DELIVERY_STATUS': "Статус доставки:",
        'WEBAPP_REQUESTED': "Запрошено:",
        'WEBAPP_YOUR_COMMENT': "Ваш комментарий:",
        'WEBAPP_CONFIRM_RECEIPT_BUTTON': "Подтвердить получение",
        'WEBAPP_BACK': "Назад",
        'WEBAPP_PARTNER_TEXT': "Сотрудничайте с JIP и получайте подарки",
        'WEBAPP_CONTACT_ADMIN': "Связаться с администратором",
        'WEBAPP_INFO_TEXT': "Баллы зачисляются на ваш счет сразу после сканирования промокода.\n\n\n\nЕсли баллы не зачислились, пожалуйста, обратитесь к администратору.",
        'WEBAPP_REGISTER': "Отправить",
        'WEBAPP_VIEW_GIFTS': "Посмотреть подарки",
        'WEBAPP_PRIVACY_POLICY': "Политика конфиденциальности",
        'WEBAPP_QR_ERROR': "Введен неверный промокод",
        'WEBAPP_QR_PLACEHOLDER': "Введите промокод",
        'WEBAPP_GIFTS_TITLE': "Подарки",
        'WEBAPP_GIFT_NAME': "Название подарка",
        'WEBAPP_GET_GIFT': "Получить подарок",
        'WEBAPP_NOT_ENOUGH_POINTS': "Недостаточно баллов",
        'WEBAPP_WAITING_PROCESS': "В процессе ожидания",
        'WEBAPP_SUCCESS_TITLE': "Успешно выполнено!",
        'WEBAPP_SUCCESS_MESSAGE': "Ваш подарок готовится, наши сотрудники свяжутся с вами в ближайшее время.",
        'WEBAPP_TO_HOME': "На главную",
        'WEBAPP_GIFT_IN_STOCK': "В наличии",
        'WEBAPP_GIFT_COST': "Стоимость",
        'WEBAPP_GIFT_AFTER_REDEMPTION': "После обмена",
        'WEBAPP_CONTACT_ADMIN_CHOOSE': "Выберите удобный способ связи",
        'WEBAPP_PROFILE': "Профиль",
        'WEBAPP_INTERFACE_LANGUAGE': "Язык интерфейса",
        'WEBAPP_GIFTS': "Мои заявки",
        'WEBAPP_QR_HISTORY': "История промокодов",
        'WEBAPP_NAV_HOME': "Главная",
        'WEBAPP_NAV_GIFTS': "Подарки",
        'WEBAPP_NAV_HISTORY': "Промокоды",
        'WEBAPP_NAV_MY_GIFTS': "Мои заявки",
        'WEBAPP_NAV_PROFILE': "Профиль",
        'WEBAPP_USER_TYPE_ELECTRICIAN': "Сантеник",
        'WEBAPP_USER_TYPE_SELLER': "Продавец",
        'WEBAPP_MY_GIFTS_MENU': "Мои заявки",
        'WEBAPP_LIVE_STREAMS_TITLE': "Прямые эфиры",
        'WEBAPP_LIVE_STREAMS_UPCOMING': "Предстоящие эфиры",
        'WEBAPP_LIVE_STREAMS_PAST': "Прошедшие эфиры",
        'WEBAPP_LIVE_STREAM_OPEN': "Открыть эфир",
        'WEBAPP_LIVE_STREAM_WATCH_RECORDING': "Смотреть запись",
        'WEBAPP_LIVE_STREAM_NO_UPCOMING': "Предстоящих эфиров нет",
        'WEBAPP_LIVE_STREAM_NO_PAST': "Прошедших эфиров нет",
        'WEBAPP_LIVE_STREAM_WINNERS_ELECTRICIANS': "Победители — сантехники",
        'WEBAPP_LIVE_STREAM_WINNERS_SELLERS': "Победители — предприниматели",
        'WEBAPP_LIVE_STREAM_NO_WINNERS': "Победители ещё не объявлены",
        'WEBAPP_LIVE_STREAM_LOADING': "Загружаем прямые эфиры...",
        'WEBAPP_MONTHLY_CHANCES': "{count} шансов",
        'WEBAPP_QR_FILTER_CURRENT_MONTH': "Этот месяц",
        'WEBAPP_QR_FILTER_ALL': "Все",
        'WEBAPP_TICKET_NUMBER': "Билет №{order}",
        'WEBAPP_TICKET_NUMBER_SHORT': "№",
        'WEBAPP_TICKET_LABEL': "БИЛЕТ",
        'WEBAPP_RAFFLE_TICKETS': "Промокоды на розыгрыш",
        'WEBAPP_RAFFLE_FINISHED': "розыгрыш завершён",
        'WEBAPP_CHANCES': "шансов",
        'WEBAPP_QR_CURRENT_MONTH_TITLE': "промокоды розыгрыша",
        'WEBAPP_QR_ARCHIVE': "архив",
        'WEBAPP_BALL_SHORT': "б",
        'WEBAPP_OPEN': "Открыть",
        'WEBAPP_PLAY': "Воспроизвести",
        'WEBAPP_PLACE': "МЕСТО",
        'WEBAPP_LIVE_RECORD': "● ЗАПИСЬ",
        'WEBAPP_LIVE_PARTICIPANTS': "Участников",
        'WEBAPP_LIVE_WINNERS': "Победителей",
        'WEBAPP_LIVE_WINNERS_TITLE': "Эфир — победители",
        'WEBAPP_LIVE_FOOTNOTE': "Победители выбраны случайно",
        'WEBAPP_TAB_ELECTRICIANS': "Сантехники",
        'WEBAPP_TAB_SELLERS': "Продавцы",
        'WEBAPP_PRIZE': "Приз",
        'WEBAPP_TOP_USERS_TITLE_ELECTRICIANS': "Топ сантехники",
        'WEBAPP_TOP_USERS_TITLE_SELLERS': "Топ продавцы",
        'WEBAPP_TOP_USERS_PERIOD_ALL': "За весь период",
        'WEBAPP_TOP_USERS_PERIOD_CURRENT': "Текущий месяц",
        'WEBAPP_TOP_USERS_EMPTY': "Нет данных",
        'WEBAPP_TOP_USERS_YOU': "Вы",
        'WEBAPP_TOP_USERS_NOT_RANKED': "—",
        'WEBAPP_TOP_USERS_POINTS_SHORT': "балл",
        'MONTHLY_CHANCES_LINE': "Ваши шансы в этом месяце: {count}",
        'WEBAPP_UZBEK': "Узбекский",
        'WEBAPP_RUSSIAN': "Русский",
        'WEBAPP_UPDATED': "Обновлено",
        'WEBAPP_CLOSE': "Закрыть",
        'WEBAPP_BALL': "Балл",
        'WEBAPP_NEXT_GIFT_LABEL': "Следующий подарок:",
        'WEBAPP_POINTS_NEEDED_MORE': "Вам нужно еще {points} баллов",
        'WEBAPP_ORDERS_TITLE': "Мои заказы",
        'WEBAPP_ORDERS_TOTAL': "{count} всего",
        'WEBAPP_ORDERS_TAB_ACTIVE': "Активные",
        'WEBAPP_ORDERS_TAB_DELIVERED': "Доставленные",
        'WEBAPP_ORDER_NUMBER': "Заказ #{n}",
        'WEBAPP_STEP_CONFIRMED': "Подтверждено",
        'WEBAPP_STEP_SHIPPED': "В пути",
        'WEBAPP_STEP_DELIVERED': "Доставлено",
        'WEBAPP_BADGE_PROCESSING': "Обработка",
        'WEBAPP_BADGE_CONFIRMED': "Подтверждён",
        'WEBAPP_BADGE_ON_THE_WAY': "В пути",
        'WEBAPP_BADGE_DELIVERED': "Доставлен",
        'WEBAPP_BADGE_RECEIVED': "Получен",
        'WEBAPP_BADGE_REJECTED': "Отклонён",
        'WEBAPP_BADGE_CANCELLED': "Вы отменили",
        'WEBAPP_BADGE_NOT_RECEIVED': "Не получен",
        'WEBAPP_ORDERS_EMPTY_TAB': "В этом разделе заказов нет",
        'WEBAPP_LOADING_QR_HISTORY': "Загрузка истории промокодов...",
        'WEBAPP_NO_QR_HISTORY': "История промокодов пуста",
        'WEBAPP_QR_MAX_ATTEMPTS': "❌ Вы сегодня {max_attempts} раз ввели неверный промокод. Следующие попытки откроются завтра (00:00).",
        'WEBAPP_QR_WRONG_TYPE': "❌ Этот промокод не соответствует вашему типу. Вы можете вводить только промокоды, соответствующие вашему типу.",
        'WEBAPP_PRIVACY_PDF_DESCRIPTION': "Политика конфиденциальности доступна в формате PDF. Нажмите кнопку ниже, чтобы открыть документ в браузере.",
        'WEBAPP_OPEN_PDF': "Открыть PDF",

        # Dashboard UI (Russian equivalents)
        'DASHBOARD_USER_OVERVIEW': "Количество пользователей",
        'DASHBOARD_ELECTRICIAN_CODES': "Количество кодов сантеников",
        'DASHBOARD_STORE_CODES': "Коды магазинов",
        'DASHBOARD_TOTAL_POINTS': "Количество баллов",
        'DASHBOARD_ELECTRICIAN_POOL': "Пул баллов сантеников",
        'DASHBOARD_STORE_POOL': "Пул баллов магазинов",
        'DASHBOARD_GIFT_REQUESTS': "Количество подарков",
        'DASHBOARD_GIFTS_ELECTRICIANS': "Подарки — Сантеники",
        'DASHBOARD_GIFTS_STORES': "Подарки — Магазины",

        'DASHBOARD_TAB_GENERAL': "Общий",
        'DASHBOARD_TAB_STORES': "Магазины в акции",
        'DASHBOARD_TAB_ELECTRICIANS': "Сантеники в акции",

        'DASHBOARD_FILTER_PERIOD': "Период:",
        'DASHBOARD_FILTER_FROM': "От",
        'DASHBOARD_FILTER_TO': "До",
        'DASHBOARD_FILTER_APPLY': "Применить",
        'DASHBOARD_FILTER_RESET': "Сбросить",
        'DASHBOARD_FILTER_ALL_TIME': "Весь период",

        'DASHBOARD_LABEL_ELECTRICIANS': "Сантеники",
        'DASHBOARD_LABEL_STORES': "Магазины",
        'DASHBOARD_LABEL_UNSELECTED': "Не выбрано",
        'DASHBOARD_LABEL_SCANNED': "Сканировано",
        'DASHBOARD_LABEL_SCANNED_TOTAL': "Всего сканировано",
        'DASHBOARD_LABEL_SCANNED_PERIOD': "Сканировано за период",
        'DASHBOARD_LABEL_SPENT': "Потрачено",
        'DASHBOARD_LABEL_REMAINING': "Не сканировано",

        'DASHBOARD_LABEL_SCANNED_TOTAL_COUNT': "Всего сканировано (кол-во)",
        'DASHBOARD_LABEL_SCANNED_PERIOD_COUNT': "Сканировано за период (кол-во)",
        'DASHBOARD_LABEL_REMAINING_COUNT': "Не сканировано (кол-во)",

        'DASHBOARD_LABEL_SCANNED_TOTAL_POINTS': "Всего сканировано (баллы)",
        'DASHBOARD_LABEL_SCANNED_PERIOD_POINTS': "Сканировано за период (баллы)",
        'DASHBOARD_LABEL_SPENT_POINTS': "Потрачено (баллы)",
        'DASHBOARD_LABEL_REMAINING_POINTS': "Не сканировано (баллы)",

        'NEW_THIS_PERIOD': "Новых за период",

        'DASHBOARD_STATUS_SUCCESS': "Выдано",
        'DASHBOARD_STATUS_PENDING': "В процессе",
        'DASHBOARD_STATUS_REJECTED': "Не выдано",

        'DASHBOARD_STATUS': "Статус",
        'DASHBOARD_TOTAL': "Всего",

        'DASHBOARD_HEADER_COUNT': "Кол-во",
        'DASHBOARD_HEADER_POINTS': "Баллы",

        'DASHBOARD_CHART_POPULAR_GIFTS': "Самые популярные подарки",
        'DASHBOARD_CHART_REQUEST_STATUSES': "Статусы запросов",
        'DASHBOARD_CHART_DISTRICT_DISTRIBUTION': "Статистика по районам",
        'DASHBOARD_CHART_REGIONAL_DISTRIBUTION': "Статистика по областям",

        # Sotuvchi asosiy menyusi (RU)
        'SELLER_MAIN_MENU': "👋 Здравствуйте, {name}!\n\n🏪 Магазин: {store}\n💰 Ваш баланс: {points} баллов\n\nВыберите действие:",
        'SELLER_MY_BALANCE': "💰 Мой баланс",
        'SELLER_SALES_HISTORY': "📊 История продаж",
        'SELLER_MY_STORE': "🏪 Мой магазин",
        'SELLER_OPEN_WEBAPP': "🌐 Открыть веб-приложение",
        'SELLER_CONTACT_ADMIN': "📞 Связаться с администратором",
        'SELLER_BALANCE_INFO': "💰 Ваш баланс: {points} баллов\n\nБаллы начисляются только администратором.",
        'SELLER_STORE_INFO': "🏪 <b>{name}</b>\n\n📍 Адрес: {address}\n📊 Регион: {region}\n\n📦 Карт: {total} шт (отсканировано: {scanned})\n💳 Комиссия: {commission}%",
        'SELLER_NO_STORE': "❗ Ваш магазин не найден. Свяжитесь с администратором.",
        'SELLER_WEBAPP_BUTTON': "📊 Панель продавца",
        'SELLER_REG_SUCCESS': (
            "✅ <b>Регистрация успешно пройдена!</b>\n\n"
            "Теперь вы можете пользоваться панелью продавца. "
            "Нажмите кнопку ниже, чтобы открыть Web App."
        ),
    },
}


def get_text(user, key, **kwargs):
    """
    Получает переведенный текст для пользователя.
    
    Args:
        user: Экземпляр TelegramUser
        key: Ключ перевода
        **kwargs: Параметры для форматирования строки
    
    Returns:
        str: Переведенный текст
    """
    language = getattr(user, 'language', 'uz_latin')
    translations = TRANSLATIONS.get(language, TRANSLATIONS['uz_latin'])
    text = translations.get(key, key)
    
    if kwargs:
        try:
            return text.format(**kwargs)
        except KeyError:
            return text
    
    return text


# Обратная совместимость - экспорт для старого кода
def _get_default_translations():
    """Возвращает переводы по умолчанию (uz_latin) для обратной совместимости."""
    return TRANSLATIONS['uz_latin']


# Экспорт констант для обратной совместимости
WELCOME = _get_default_translations()['WELCOME']
SEND_PHONE = _get_default_translations()['SEND_PHONE']
PHONE_SAVED = _get_default_translations()['PHONE_SAVED']
SEND_LOCATION = _get_default_translations()['SEND_LOCATION']
REGISTRATION_COMPLETE = _get_default_translations()['REGISTRATION_COMPLETE']
USE_BUTTON_PHONE = _get_default_translations()['USE_BUTTON_PHONE']
USE_BUTTON_LOCATION = _get_default_translations()['USE_BUTTON_LOCATION']
QR_ACTIVATED = _get_default_translations()['QR_ACTIVATED']
QR_MAX_ATTEMPTS = _get_default_translations()['QR_MAX_ATTEMPTS']
QR_NOT_FOUND = _get_default_translations()['QR_NOT_FOUND']
QR_ALREADY_SCANNED = _get_default_translations()['QR_ALREADY_SCANNED']
QR_ERROR = _get_default_translations()['QR_ERROR']
MAIN_MENU = _get_default_translations()['MAIN_MENU']
MY_GIFTS = _get_default_translations()['MY_GIFTS']
GIFTS = _get_default_translations()['GIFTS']
MY_BALANCE = _get_default_translations()['MY_BALANCE']
TOP_LEADERS = _get_default_translations()['TOP_LEADERS']
BALANCE_INFO = _get_default_translations()['BALANCE_INFO']
NO_GIFTS = _get_default_translations()['NO_GIFTS']
GIFTS_LIST = _get_default_translations()['GIFTS_LIST']
NO_LEADERS = _get_default_translations()['NO_LEADERS']
ERROR_OCCURRED = _get_default_translations()['ERROR_OCCURRED']
