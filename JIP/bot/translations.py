"""
Bot UI translation strings.

Tildi kalit so'zi sifatida `uz_latin` va `ru` ishlatiladi. Yangi tarjima
qo'shganda ikkala tildagi qiymatni bering.
"""
from __future__ import annotations


TRANSLATIONS: dict[str, dict[str, str]] = {
    'uz_latin': {
        # Welcome / language
        'choose_language': "Tilni tanlang / Выберите язык:",
        'lang_chosen': "Til tanlandi: O'zbekcha 🇺🇿",
        'welcome': (
            "Salom! JIP sodiqlik dasturiga xush kelibsiz.\n\n"
            "Ro'yxatdan o'tish uchun bir nechta savolga javob bering."
        ),

        # Registration
        'ask_name': "Ismingizni kiriting:",
        'ask_user_type': "Kim siz?",
        'btn_santenik': "🔧 Santenik",
        'btn_sotuvchi': "🏪 Sotuvchi",
        'ask_privacy': (
            "Maxfiylik siyosati va shartlariga rozimisiz?\n\n"
            "Davom etish uchun rozilik bering."
        ),
        'btn_agree': "✅ Roziman",
        'btn_disagree': "❌ Rozi emasman",
        'privacy_required': "Botdan foydalanish uchun rozilik berish shart.",
        'ask_phone': "Telefon raqamingizni yuboring:",
        'btn_share_phone': "📱 Telefon raqamni yuborish",
        'ask_location': "Joylashuvingizni yuboring (live lokatsiya yoki manual):",
        'btn_share_location': "📍 Joylashuvni yuborish",

        # Store confirmation (sotuvchi)
        'store_found': "Sizning do'koningiz: «{store}». Tasdiqlaysizmi?",
        'btn_yes': "✅ Ha",
        'btn_no': "❌ Yo'q",
        'store_not_found': (
            "Telefon raqamingiz bo'yicha do'kon topilmadi.\n"
            "Iltimos, admin bilan bog'laning: {support}"
        ),
        'wait_admin_link_seller': (
            "Adminni do'koningizga biriktirishini kutamiz.\n"
            "Admin: {support}"
        ),
        'registration_complete': "Ro'yxatdan o'tish tugadi. Marhamat:",

        # Santenik menu
        'menu_balance': "💰 Mening ballarim",
        'menu_gifts': "🎁 Sovg'alar",
        'menu_orders': "📦 Mening buyurtmalarim",
        'menu_top_month': "🏆 Top 10 (oy)",
        'menu_top_all': "🏆 Top 10 (umumiy)",
        'menu_video': "📹 Yo'riqnoma video",
        'menu_language': "🌐 Til",
        'menu_help': "ℹ️ Yordam",

        # Sotuvchi menu
        'menu_my_balance': "💰 Mening balansim",
        'menu_sales_history': "📊 Sotuv tarixim",
        'menu_my_store': "📦 Mening do'konim",
        'menu_webapp': "🌐 Web App",
        'menu_admin_contact': "ℹ️ Admin bilan bog'lanish",

        # Promo code (QR scan)
        'promo_success': (
            "✅ +{points} ball qo'shildi!\n\n"
            "🏪 Karta manbai: «{store}» do'koni\n"
            "💰 Joriy balans: {balance} ball\n\n"
            "🎁 Sovg'alarni ko'rishni xohlaysizmi?"
        ),
        'promo_invalid': "❌ Bunday kod topilmadi. Tekshirib qaytadan kiriting.",
        'promo_used': "❌ Bu karta allaqachon ishlatilgan.",
        'promo_blocked': "🚫 Siz vaqtinchalik bloklangan ekansiz. {until} dan keyin urinib ko'ring.",
        'promo_wrong_role': "❌ Sizning rolingiz bu kodni faollashtira olmaydi.",

        # Balance / general
        'balance_info': "💰 Joriy balans: {balance} ball",
        'no_data': "Ma'lumot topilmadi.",
        'error_generic': "Xatolik yuz berdi. Keyinroq urinib ko'ring.",
        'language_changed': "Til o'zgartirildi: O'zbekcha 🇺🇿",
        'help_text': (
            "JIP sodiqlik dasturi yordami.\n\n"
            "• Skretch-kartani tirnab, kodni shu yerga kiriting\n"
            "• Ballarni sovg'aga ayirboshlang\n"
            "• Savol bo'lsa adminga yozing: {support}"
        ),
    },
    'ru': {
        # Welcome
        'choose_language': "Tilni tanlang / Выберите язык:",
        'lang_chosen': "Язык выбран: Русский 🇷🇺",
        'welcome': (
            "Здравствуйте! Добро пожаловать в программу лояльности JIP.\n\n"
            "Ответьте на несколько вопросов для регистрации."
        ),

        # Registration
        'ask_name': "Введите ваше имя:",
        'ask_user_type': "Кто вы?",
        'btn_santenik': "🔧 Сантехник",
        'btn_sotuvchi': "🏪 Продавец",
        'ask_privacy': (
            "Согласны ли вы с политикой конфиденциальности?\n\n"
            "Для продолжения дайте согласие."
        ),
        'btn_agree': "✅ Согласен",
        'btn_disagree': "❌ Не согласен",
        'privacy_required': "Для использования бота необходимо согласие.",
        'ask_phone': "Отправьте ваш номер телефона:",
        'btn_share_phone': "📱 Отправить номер",
        'ask_location': "Отправьте ваше местоположение (live геолокация или вручную):",
        'btn_share_location': "📍 Отправить геолокацию",

        # Store confirmation
        'store_found': "Ваш магазин: «{store}». Подтверждаете?",
        'btn_yes': "✅ Да",
        'btn_no': "❌ Нет",
        'store_not_found': (
            "По вашему номеру магазин не найден.\n"
            "Пожалуйста, свяжитесь с админом: {support}"
        ),
        'wait_admin_link_seller': (
            "Ожидайте, пока админ привяжет вас к магазину.\n"
            "Админ: {support}"
        ),
        'registration_complete': "Регистрация завершена. Меню:",

        # Santenik menu
        'menu_balance': "💰 Мои баллы",
        'menu_gifts': "🎁 Подарки",
        'menu_orders': "📦 Мои заказы",
        'menu_top_month': "🏆 Топ 10 (месяц)",
        'menu_top_all': "🏆 Топ 10 (всего)",
        'menu_video': "📹 Видеоинструкция",
        'menu_language': "🌐 Язык",
        'menu_help': "ℹ️ Помощь",

        # Sotuvchi menu
        'menu_my_balance': "💰 Мой баланс",
        'menu_sales_history': "📊 История продаж",
        'menu_my_store': "📦 Мой магазин",
        'menu_webapp': "🌐 Web App",
        'menu_admin_contact': "ℹ️ Связаться с админом",

        # Promo code
        'promo_success': (
            "✅ +{points} баллов добавлено!\n\n"
            "🏪 Источник: магазин «{store}»\n"
            "💰 Текущий баланс: {balance} баллов\n\n"
            "🎁 Хотите посмотреть подарки?"
        ),
        'promo_invalid': "❌ Такой код не найден. Проверьте и введите снова.",
        'promo_used': "❌ Эта карта уже использована.",
        'promo_blocked': "🚫 Вы временно заблокированы. Попробуйте после {until}.",
        'promo_wrong_role': "❌ Ваша роль не может активировать этот код.",

        # General
        'balance_info': "💰 Текущий баланс: {balance} баллов",
        'no_data': "Данные не найдены.",
        'error_generic': "Произошла ошибка. Попробуйте позже.",
        'language_changed': "Язык изменён: Русский 🇷🇺",
        'help_text': (
            "Справка по программе лояльности JIP.\n\n"
            "• Сотрите скретч-полосу и введите код сюда\n"
            "• Обменивайте баллы на подарки\n"
            "• Вопросы → админу: {support}"
        ),
    },
}


def t(language: str, key: str, **kwargs) -> str:
    """Get translated string with optional formatting."""
    pack = TRANSLATIONS.get(language) or TRANSLATIONS['uz_latin']
    text = pack.get(key) or TRANSLATIONS['uz_latin'].get(key) or key
    if kwargs:
        try:
            return text.format(**kwargs)
        except (KeyError, IndexError):
            return text
    return text
