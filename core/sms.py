"""Eskiz.uz SMS gateway — async klient (OTP yuborish uchun).

Birlamchi vazifa: ro'yxatdan o'tishda tasdiqlash kodini real SMS orqali yuborish.
API: https://notify.eskiz.uz/api
  - POST /auth/login   (email, password) -> data.token (30 kun)
  - POST /message/sms/send  (mobile_phone, message, from) + Bearer token

Token Django cache'da saqlanadi (best-effort, Redis restart bo'lsa qayta login).
401 kelsa -> token tozalanadi, qayta login + 1 marta retry.
"""
import asyncio
import logging
import re

import aiohttp
from asgiref.sync import sync_to_async
from django.conf import settings
from django.core.cache import cache

logger = logging.getLogger(__name__)

ESKIZ_BASE = "https://notify.eskiz.uz/api"
_TOKEN_CACHE_KEY = "eskiz_token"
_TOKEN_TTL = 29 * 24 * 3600  # 29 kun (< 30 kunlik amal muddati)
_HTTP_TIMEOUT = aiohttp.ClientTimeout(total=15)


def _normalize_phone(phone: str) -> str:
    """'+998901234567' / '998 90 123 45 67' -> '998901234567' (faqat raqam, + yo'q)."""
    return re.sub(r"\D", "", phone or "")


def _is_valid_uz_mobile(digits: str) -> bool:
    """998 + 9 raqam == 12 ta belgi."""
    return len(digits) == 12 and digits.startswith("998")


async def _cache_get(key):
    return await sync_to_async(cache.get)(key)


async def _cache_set(key, value, ttl):
    await sync_to_async(cache.set)(key, value, ttl)


async def _cache_delete(key):
    await sync_to_async(cache.delete)(key)


async def eskiz_login() -> str | None:
    """POST /auth/login -> token. Tokenni cache'ga yozadi. Token yoki None qaytaradi."""
    email = getattr(settings, "ESKIZ_EMAIL", "")
    password = getattr(settings, "ESKIZ_PASSWORD", "")
    if not email or not password:
        logger.error("Eskiz creds yo'q (ESKIZ_EMAIL / ESKIZ_PASSWORD)")
        return None
    url = f"{ESKIZ_BASE}/auth/login"
    try:
        async with aiohttp.ClientSession(timeout=_HTTP_TIMEOUT) as sess:
            async with sess.post(url, data={"email": email, "password": password}) as resp:
                data = await resp.json(content_type=None)
                if resp.status != 200:
                    logger.error("Eskiz login failed status=%s body=%s", resp.status, data)
                    return None
        token = (data.get("data") or {}).get("token")
        if not token:
            logger.error("Eskiz login: javobda token yo'q: %s", data)
            return None
    except Exception as e:
        logger.warning("Eskiz login exception: %s", e)
        return None
    # Cache'ga yozish — xato bo'lsa ham token qaytadi (cache ikkilamchi).
    try:
        await _cache_set(_TOKEN_CACHE_KEY, token, _TOKEN_TTL)
    except Exception as e:
        logger.warning("Eskiz token cache'lanmadi (zarar yo'q): %s", e)
    logger.info("Eskiz login OK")
    return token


async def eskiz_send_sms(phone: str, message: str) -> tuple[bool, str]:
    """Bitta SMS yuboradi.

    Qaytaradi (ok, info). Muvaffaqiyatда info = Eskiz message id.
    Xato turlari: 'invalid_phone' | 'no_token' | 'timeout' | 'http_<code>' | 'error:<msg>'.
    Token cache -> miss bo'lsa login -> 401 bo'lsa qayta login + 1 retry.
    """
    digits = _normalize_phone(phone)
    if not _is_valid_uz_mobile(digits):
        logger.warning("Eskiz: noto'g'ri telefon %r -> %r", phone, digits)
        return False, "invalid_phone"

    try:
        token = await _cache_get(_TOKEN_CACHE_KEY)
    except Exception as e:
        logger.warning("Eskiz cache get xato: %s", e)
        token = None
    if not token:
        token = await eskiz_login()
        if not token:
            return False, "no_token"

    sender = getattr(settings, "ESKIZ_FROM", "4546")

    async def _do_send(tok: str):
        url = f"{ESKIZ_BASE}/message/sms/send"
        payload = {"mobile_phone": digits, "message": message, "from": sender}
        headers = {"Authorization": f"Bearer {tok}"}
        async with aiohttp.ClientSession(timeout=_HTTP_TIMEOUT) as sess:
            async with sess.post(url, data=payload, headers=headers) as resp:
                body = await resp.json(content_type=None)
                return resp.status, body

    try:
        status, body = await _do_send(token)

        # 401 / token eskirgan -> qayta login + 1 marta retry
        if status == 401:
            logger.info("Eskiz 401 -> qayta login + retry")
            await _cache_delete(_TOKEN_CACHE_KEY)
            token = await eskiz_login()
            if not token:
                return False, "no_token"
            status, body = await _do_send(token)

        if status in (200, 201):
            if isinstance(body, dict) and str(body.get("status", "")).lower() == "error":
                logger.warning("Eskiz send rad etildi: %s", body)
                return False, "error:" + str(body.get("message") or body)
            msg_id = body.get("id") if isinstance(body, dict) else ""
            logger.info("Eskiz send OK phone=%s id=%s", digits, msg_id)
            return True, str(msg_id or "")

        logger.warning("Eskiz send http=%s body=%s", status, body)
        return False, f"http_{status}"

    except asyncio.TimeoutError:
        logger.warning("Eskiz send timeout phone=%s", digits)
        return False, "timeout"
    except Exception as e:
        logger.warning("Eskiz send exception: %s", e)
        return False, "error:" + str(e)
