"""
Telegram WebApp init data HMAC tekshiruvi — TZ §7.4.

Reference: https://core.telegram.org/bots/webapps#validating-data-received-via-the-mini-app
"""
from __future__ import annotations

import hashlib
import hmac
import json
import time
from typing import Optional
from urllib.parse import parse_qsl

from django.conf import settings


MAX_AGE_SECONDS = 24 * 60 * 60  # 24 soat


def parse_init_data(init_data: str) -> dict:
    """tg.initData query-string'ni dict'ga aylantiradi."""
    return dict(parse_qsl(init_data, keep_blank_values=True))


def verify_init_data(init_data: str, bot_token: Optional[str] = None) -> Optional[dict]:
    """
    initData tekshiriladi. Muvaffaqiyat — parsed dict (user, auth_date, hash).
    Xato — None.
    """
    if not init_data:
        return None

    token = bot_token or getattr(settings, 'TELEGRAM_BOT_TOKEN', '')
    if not token:
        return None

    parsed = parse_init_data(init_data)
    received_hash = parsed.pop('hash', None)
    if not received_hash:
        return None

    # auth_date eskirganligini tekshir
    try:
        auth_date = int(parsed.get('auth_date', '0'))
    except ValueError:
        return None
    if auth_date and (time.time() - auth_date) > MAX_AGE_SECONDS:
        return None

    data_check_string = '\n'.join(f'{k}={v}' for k, v in sorted(parsed.items()))
    secret_key = hmac.new(b'WebAppData', token.encode(), hashlib.sha256).digest()
    calculated_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()

    if not hmac.compare_digest(calculated_hash, received_hash):
        return None

    if 'user' in parsed:
        try:
            parsed['user'] = json.loads(parsed['user'])
        except (json.JSONDecodeError, TypeError):
            pass
    return parsed


def get_telegram_user_from_request(request) -> Optional[dict]:
    """Header yoki query param'dan init data oladi va tekshiradi."""
    init_data = request.headers.get('X-Telegram-Init-Data') or request.GET.get('initData', '')
    return verify_init_data(init_data)
