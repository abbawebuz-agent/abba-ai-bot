"""
Базовые настройки Django для проекта mona.
Общие настройки для всех окружений.
"""
import logging
import os
from pathlib import Path
import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Load environment variables
env = environ.Env(
    DEBUG=(bool, False)
)
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY', default='django-insecure-change-this-in-production')

# Application definition
INSTALLED_APPS = [
    # Unfold — django.contrib.admin dan OLDIN bo'lishi shart
    'unfold',
    'unfold.contrib.filters',
    'unfold.contrib.forms',
    'unfold.contrib.inlines',
    'unfold.contrib.simple_history',  # simple_history bilan integratsiya
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'channels',
    'simple_history',  # История изменений моделей
    'rangefilter',  # Фильтр по диапазону дат в админке
    'corsheaders',
    'rest_framework_simplejwt',
    'core',
    'bot',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # WhiteNoise для статических файлов
    'core.middleware.NoCacheMiddleware',  # Отключение кеша для Telegram Web App
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',  # Поддержка локализации
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'simple_history.middleware.HistoryRequestMiddleware',  # Отслеживание пользователя для истории
    'core.middleware.CurrentRequestMiddleware',  # ActivityLog signals uchun thread-local
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# django-simple-history: причина изменения в истории — текстовое поле (без ограничения 100 символов)
SIMPLE_HISTORY_HISTORY_CHANGE_REASON_USE_TEXT_FIELD = True

ROOT_URLCONF = 'mona.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'mona.wsgi.application'
ASGI_APPLICATION = 'mona.asgi.application'

# Database — Railway DATABASE_URL yoki alohida DB_* qiymatlarni qo'llab-quvvatlash
_db_url = env('DATABASE_URL', default='')
if _db_url:
    try:
        import dj_database_url
        DATABASES = {'default': dj_database_url.parse(_db_url, conn_max_age=600)}
    except ImportError:
        import urllib.parse as _urlparse
        _u = _urlparse.urlparse(_db_url)
        DATABASES = {'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': _u.path.lstrip('/'),
            'USER': _u.username or '',
            'PASSWORD': _u.password or '',
            'HOST': _u.hostname or 'localhost',
            'PORT': str(_u.port or 5432),
            'CONN_MAX_AGE': 600,
        }}
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': env('DB_NAME', default='mona_db'),
            'USER': env('DB_USER', default='mona_user'),
            'PASSWORD': env('DB_PASSWORD', default='mona_password'),
            'HOST': env('DB_HOST', default='db'),
            'PORT': env('DB_PORT', default='5432'),
        }
    }

# MongoDB Configuration
MONGODB_SETTINGS = {
    'host': env('MONGODB_HOST', default='mongodb'),
    'port': int(env('MONGODB_PORT', default='27017')),
    'db': env('MONGODB_DB', default='mona_mongodb'),
}

# Redis — Railway REDIS_URL yoki alohida REDIS_HOST/PORT
# BUG-023 FIX: agar REDIS_URL berilgan bo'lsa, uni to'g'ridan-to'g'ri ishlatamiz
# (host/port qisib olishga urinish kerak emas — auth bilan URL buziladi).
_redis_url = env('REDIS_URL', default='')
if _redis_url:
    # URL dan host/port ajratib olish (channels_redis tuple talab qiladi)
    from urllib.parse import urlparse as _urlparse
    _parsed = _urlparse(_redis_url)
    REDIS_HOST = _parsed.hostname or 'redis'
    REDIS_PORT = _parsed.port or 6379
    # Cache, Celery, Channels — barchasi to'liq URL ishlatadi (parol bilan)
    _redis_base = _redis_url.rstrip('/')
    if _redis_base.endswith(('/0', '/1', '/2', '/3', '/4', '/5')):
        # Agar URL allaqachon DB nomeriga ega bo'lsa — base'ni olamiz
        _redis_base = _redis_base.rsplit('/', 1)[0]
    CELERY_BROKER_URL = f'{_redis_base}/0'
    CELERY_RESULT_BACKEND = f'{_redis_base}/0'
    _cache_location = f'{_redis_base}/1'
else:
    REDIS_HOST = env('REDIS_HOST', default='redis')
    REDIS_PORT = int(env('REDIS_PORT', default='6379'))
    CELERY_BROKER_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}/0'
    CELERY_RESULT_BACKEND = f'redis://{REDIS_HOST}:{REDIS_PORT}/0'
    _cache_location = f'redis://{REDIS_HOST}:{REDIS_PORT}/1'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60  # 30 minutes
CELERY_TASK_SOFT_TIME_LIMIT = 25 * 60  # 25 minutes

# Cache Configuration (Redis) — Django 5.0 built-in RedisCache
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': _cache_location,
    }
}

# Channels
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [(REDIS_HOST, REDIS_PORT)],
        },
    },
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization — мультиязычность в админке, основной язык узбекский
# Django использует стандартные ISO 639 коды, но мы храним кастомные коды в БД
# Маппинг: uz_latin -> uz, ru -> ru
LANGUAGE_CODE = 'uz'  # Основной язык по умолчанию — узбекский
LANGUAGES = [
    ('uz', "O'zbek"),   # Основной язык (узбекский)
    ('ru', 'Русский'),
    ('en', 'English'),  # Для админки (полные переводы Django)
]
LOCALE_PATHS = [
    BASE_DIR / 'locale',
]
TIME_ZONE = 'Asia/Tashkent'  # Временная зона Узбекистана
USE_I18N = True
USE_TZ = True
USE_L10N = True

# Celery Timezone (должно быть после определения TIME_ZONE)
CELERY_TIMEZONE = TIME_ZONE

from celery.schedules import crontab as _crontab

# Расписание Celery Beat
CELERY_BEAT_SCHEDULE = {
    # Раз в минуту проверяем БД на отложенные региональные рассылки.
    # Источник правды — RegionMessageLog (status='pending'), поэтому очередь
    # переживает перезапуск Redis/воркеров.
    'dispatch-scheduled-region-messages': {
        'task': 'core.tasks.dispatch_scheduled_region_messages',
        'schedule': 60.0,  # секунд
    },
    # 1-го числа каждого месяца, каждые 15 минут — push-напоминание
    # пользователям без выбранной роли / с незавершённой регистрацией.
    # Сам таск проверяет time_of_day из настроек и не запустится дважды
    # благодаря уникальному month_key в MonthlyReminderLog.
    'dispatch-monthly-role-reminder': {
        'task': 'core.tasks.dispatch_monthly_role_reminder',
        'schedule': _crontab(minute='*/15', day_of_month='1'),
    },
    # Har kuni 04:00 (Asia/Tashkent) — DB backup → Telegram channel
    'daily-db-backup': {
        'task': 'core.tasks.daily_db_backup',
        'schedule': _crontab(hour=4, minute=0),
    },
}

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Additional locations of static files
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'core', 'static'),
]

# WhiteNoise configuration для статических файлов
# Используем CompressedStaticFilesStorage вместо CompressedManifestStaticFilesStorage
# для более надежной работы (manifest может вызывать проблемы если не собран правильно)
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Настройки для загрузки больших файлов (видео инструкции)
FILE_UPLOAD_MAX_MEMORY_SIZE = 52428800  # 50MB - файлы больше этого размера будут сохраняться на диск
DATA_UPLOAD_MAX_MEMORY_SIZE = 524288000  # 500MB - максимальный размер данных в запросе
DATA_UPLOAD_MAX_NUMBER_FIELDS = 10000  # Увеличиваем лимит полей в форме

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Telegram Bot Token
TELEGRAM_BOT_TOKEN = env('TELEGRAM_BOT_TOKEN', default='')
TELEGRAM_BOT_USERNAME = env('TELEGRAM_BOT_USERNAME', default='')  # @username бота (без @)
TELEGRAM_BOT_ADMIN_USERNAME = env('TELEGRAM_BOT_ADMIN_USERNAME', default='')  # @username администратора (без @)
# Admin Telegram IDs — sotuvchi ro'yxatdan o'tganda bildirishnoma yuboriladi
# Bir nechta ID vergul bilan: "123456789,987654321"
ADMIN_TELEGRAM_IDS = [
    int(x.strip()) for x in env('ADMIN_TELEGRAM_IDS', default='').split(',')
    if x.strip().isdigit()
]

# Backup channel — DB backuplar shu private kanalga yuboriladi
# Chat ID format: "-100xxxxxxxxxx" (channel) yoki user ID
BACKUP_CHANNEL_ID = env('BACKUP_CHANNEL_ID', default='')

# Webhook Settings (для production)
WEBHOOK_URL = env('WEBHOOK_URL', default='')
WEBHOOK_PATH = env('WEBHOOK_PATH', default=f'/webhook/{TELEGRAM_BOT_TOKEN}')
WEBHOOK_HOST = env('WEBHOOK_HOST', default='0.0.0.0')
WEBHOOK_PORT = int(env('WEBHOOK_PORT', default='8443'))

# Web App Settings
WEB_APP_URL = env('WEB_APP_URL', default='')  # HTTPS URL для Web App (можно использовать ngrok для тестирования)

# Локальный Nominatim (Docker + OSM PBF Узбекистана). Пусто — только эвристика по координатам.
NOMINATIM_BASE_URL = env('NOMINATIM_BASE_URL', default='').rstrip('/')
NOMINATIM_TIMEOUT = int(env('NOMINATIM_TIMEOUT', default='10'))
NOMINATIM_USER_AGENT = env('NOMINATIM_USER_AGENT', default='mona-bot/1.0 (private nominatim)')

# GeoJSON с multipolygons (boundary=administrative, admin_level=6) из того же PBF, что и Nominatim.
# Пусто — ищется файл osm-data/uzbekistan_admin6.geojson при наличии.
# Сборка: ogr2ogr -f GeoJSON uzbekistan_admin6.geojson uzbekistan.osm.pbf multipolygons \
#   -where "boundary='administrative' AND admin_level='6'"
UZ_ADMIN_BOUNDARIES_GEOJSON = env('UZ_ADMIN_BOUNDARIES_GEOJSON', default='').strip()

# Scratch Card Points
ELECTRICIAN_POINTS = 50  # 50 dollars
SELLER_POINTS = 20  # 20 dollars

# QR Code Settings
QR_CODE_MAX_ATTEMPTS = 5  # Максимальное количество неудачных попыток в день
QR_CODE_BATCH_SIZE = 200  # Размер батча для генерации QR-кодов (для избежания таймаутов)

# REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 50,
}

# ──────────────────────────────────────────────
# Sentry — инициализируется только если задан DSN
# ──────────────────────────────────────────────
SENTRY_DSN = env('SENTRY_DSN', default='')

if SENTRY_DSN:
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration
    from sentry_sdk.integrations.logging import LoggingIntegration
    from sentry_sdk.integrations.redis import RedisIntegration

    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[
            DjangoIntegration(
                transaction_style='url',
                middleware_spans=True,
                signals_spans=False,
            ),
            LoggingIntegration(
                level=logging.INFO,        # захватывать INFO+ как breadcrumbs
                event_level=logging.ERROR, # отправлять ERROR+ как события
            ),
            RedisIntegration(),
        ],
        traces_sample_rate=float(env('SENTRY_TRACES_SAMPLE_RATE', default='0.1')),
        environment=env('SENTRY_ENVIRONMENT', default='development'),
        send_default_pii=False,
        release=env('APP_VERSION', default=None),
    )

# CORS
CORS_ALLOWED_ORIGINS = [
    'http://localhost:5173',
    'http://localhost:3000',
    "https://web.telegram.org",
    "https://telegram.org",
]
CORS_ALLOW_CREDENTIALS = True

# Simple JWT
from datetime import timedelta as _timedelta
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': _timedelta(hours=12),
    'REFRESH_TOKEN_LIFETIME': _timedelta(days=7),
}

# CSRF для Telegram Web App
CSRF_TRUSTED_ORIGINS = [
    "https://web.telegram.org",
    "https://telegram.org",
]

# Admin redirect after login
LOGIN_REDIRECT_URL = '/admin/'
LOGIN_URL = '/admin/login/'

# ============================================================
# UNFOLD Admin Configuration (modern branch)
# ============================================================
from django.templatetags.static import static
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

def environment_callback(request):
    """Admin panelda environment badge ko'rsatadi"""
    return ["Production", "danger"]

UNFOLD = {
    "SITE_TITLE": "JIP GROUP",
    "SITE_HEADER": "JIP GROUP — Sodiqlik dasturi",
    "SITE_SUBHEADER": "Boshqaruv paneli",
    "SITE_URL": "/",
    "SITE_ICON": lambda request: static("core_admin/img/favicon.png"),
    "SITE_LOGO": lambda request: static("core_admin/img/jip_group_admin.jpg"),
    "SITE_LOGO_COLLAPSED": lambda request: static("core_admin/img/favicon.png"),
    "SITE_SYMBOL": "security",
    "SITE_FAVICONS": [
        {
            "rel": "icon",
            "sizes": "32x32",
            "type": "image/png",
            "href": lambda request: static("core_admin/img/favicon.png"),
        },
    ],
    "SHOW_HISTORY": True,
    "SHOW_VIEW_ON_SITE": True,
    "SHOW_BACK_BUTTON": True,
    "ENVIRONMENT": "mona.settings.base.environment_callback",
    "DASHBOARD_CALLBACK": "core.admin_callbacks.dashboard_callback",

    # ── Rang palitra (JIP violet/indigo) ──────────────────
    "COLORS": {
        "font": {
            "subtle-light": "107 114 128",
            "subtle-dark": "156 163 175",
            "default-light": "75 85 99",
            "default-dark": "209 213 219",
            "important-light": "17 24 39",
            "important-dark": "243 244 246",
        },
        "primary": {
            "50":  "238 242 255",
            "100": "224 231 255",
            "200": "199 210 254",
            "300": "165 180 252",
            "400": "129 140 248",
            "500": "99 102 241",   # indigo-500
            "600": "79 70 229",    # indigo-600 (asosiy)
            "700": "67 56 202",
            "800": "55 48 163",
            "900": "49 46 129",
            "950": "30 27 75",
        },
    },

    # ── Extensions ──────────────────────────────────────────
    "EXTENSIONS": {
        "modeltranslation": {
            "flags": {"uz": "🇺🇿", "ru": "🇷🇺"},
        },
    },

    # ── Sidebar Navigation ──────────────────────────────────
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": False,
        "navigation": [
            {
                "title": _("Boshqaruv"),
                "separator": True,
                "collapsible": False,
                "items": [
                    {
                        "title": _("Bosh sahifa"),
                        "icon": "home",
                        "link": reverse_lazy("admin:index"),
                    },
                    {
                        "title": _("Foydalanuvchilar"),
                        "icon": "group",
                        "link": reverse_lazy("admin:auth_user_changelist"),
                    },
                ],
            },
            {
                "title": _("Santexniklar"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Telegram foydalanuvchilar"),
                        "icon": "person",
                        "link": reverse_lazy("admin:core_telegramuser_changelist"),
                    },
                    {
                        "title": _("Sotuvchi IDlari"),
                        "icon": "badge",
                        "link": reverse_lazy("admin:core_sellerregistrationcode_changelist"),
                    },
                ],
            },
            {
                "title": _("Partiyalar & Tranzaksiyalar"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Partiyalar"),
                        "icon": "inventory_2",
                        "link": reverse_lazy("admin:core_qrcodebatch_changelist"),
                    },
                    {
                        "title": _("Skretch-kartalar"),
                        "icon": "qr_code",
                        "link": reverse_lazy("admin:core_qrcode_changelist"),
                    },
                    {
                        "title": _("Sotuvchi tranzaksiyalari"),
                        "icon": "payments",
                        "link": reverse_lazy("admin:core_sellerpointstransaction_changelist"),
                    },
                ],
            },
            {
                "title": _("Sovg'alar"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Sovg'alar ro'yxati"),
                        "icon": "card_giftcard",
                        "link": reverse_lazy("admin:core_gift_changelist"),
                    },
                    {
                        "title": _("Sovg'alarni olish"),
                        "icon": "redeem",
                        "link": reverse_lazy("admin:core_giftredemption_changelist"),
                    },
                ],
            },
            {
                "title": _("Xabarlar"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Jonli efirlar"),
                        "icon": "live_tv",
                        "link": reverse_lazy("admin:core_livestream_changelist"),
                    },
                    {
                        "title": _("Videoinstruksiyalar"),
                        "icon": "play_circle",
                        "link": reverse_lazy("admin:core_videoinstruction_changelist"),
                    },
                    {
                        "title": _("Maxfiylik siyosati"),
                        "icon": "policy",
                        "link": reverse_lazy("admin:core_privacypolicy_changelist"),
                    },
                    {
                        "title": _("Admin kontakt sozlamalari"),
                        "icon": "contact_phone",
                        "link": reverse_lazy("admin:core_admincontactsettings_changelist"),
                    },
                ],
            },
            {
                "title": _("Tizim"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Faollik tarixi"),
                        "icon": "history",
                        "link": reverse_lazy("admin:core_activitylog_changelist"),
                    },
                    {
                        "title": _("📥 Backup → Telegram"),
                        "icon": "cloud_upload",
                        "link": "/admin/backup-now/",
                    },
                    {
                        "title": _("Promo-kodni yaratish"),
                        "icon": "qr_code_2",
                        "link": "/admin/core/qrcode/generate/",
                    },
                ],
            },
        ],
    },

    # ── Tabs (change form uchun) ─────────────────────────────
    "TABS": [],
}

