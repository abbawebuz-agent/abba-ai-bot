"""
Продакшн настройки.
Используется когда DJANGO_SETTINGS_MODULE=mona.settings.production
"""
from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG', default=False)

_allowed = env.list('ALLOWED_HOSTS', default=[])

# Railway avtomatik RAILWAY_PUBLIC_DOMAIN beradi
_railway_domain = os.environ.get('RAILWAY_PUBLIC_DOMAIN', '')
if _railway_domain and _railway_domain not in _allowed:
    _allowed.append(_railway_domain)

# WEBHOOK_URL domenini ham qo'shamiz
_webhook = os.environ.get('WEBHOOK_URL', '')
if _webhook:
    import urllib.parse
    _wh_host = urllib.parse.urlparse(_webhook).hostname
    if _wh_host and _wh_host not in _allowed:
        _allowed.append(_wh_host)

# Railway healthcheck domenini qo'shamiz
if 'healthcheck.railway.app' not in _allowed:
    _allowed.append('healthcheck.railway.app')

ALLOWED_HOSTS = _allowed or ['*']

# Security settings для production
if not DEBUG:
    # Настройки для работы за прокси (nginx)
    # Django должен доверять заголовкам от прокси-сервера
    # Внешний nginx передает X-Forwarded-Proto: https
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    USE_X_FORWARDED_HOST = True
    USE_X_FORWARDED_PORT = True
    
    # Отключаем SECURE_SSL_REDIRECT, так как внешний nginx уже делает редирект с HTTP на HTTPS
    # Если включить SECURE_SSL_REDIRECT=True, Django будет пытаться редиректить HTTP->HTTPS,
    # но так как запрос от прокси приходит по HTTP, это создаст бесконечный цикл редиректов
    SECURE_SSL_REDIRECT = env.bool('SECURE_SSL_REDIRECT', default=False)
    
    # Cookie security (работают только если SECURE_PROXY_SSL_HEADER настроен правильно)
    SESSION_COOKIE_SECURE = env.bool('SESSION_COOKIE_SECURE', default=True)
    CSRF_COOKIE_SECURE = env.bool('CSRF_COOKIE_SECURE', default=True)
    
    # Другие security настройки
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'

# Логирование для production
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'django.log'),
            'maxBytes': 1024 * 1024 * 10,  # 10 MB
            'backupCount': 5,
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
        'bot': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

_log_dir = os.path.join(BASE_DIR, 'logs')
try:
    os.makedirs(_log_dir, exist_ok=True)
except OSError:
    # Railway read-only filesystem — faqat console logga yozamiz
    LOGGING['root']['handlers'] = ['console']
    for _l in LOGGING.get('loggers', {}).values():
        _l['handlers'] = ['console']

# Railway da nginx yo'q — WhiteNoise orqali statik fayllar beriladi.
# Nginx bilan deploy qilganda DISABLE_WHITENOISE=True qo'ying.
if env.bool('DISABLE_WHITENOISE', default=False):
    MIDDLEWARE = [m for m in MIDDLEWARE if m != 'whitenoise.middleware.WhiteNoiseMiddleware']

