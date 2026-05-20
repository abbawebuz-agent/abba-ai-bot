"""
Django webhook view — Telegram update'larni qabul qiladi.
"""
from __future__ import annotations

import asyncio
import json
import logging

from aiogram.types import Update
from django.conf import settings
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

logger = logging.getLogger(__name__)


@csrf_exempt
@require_POST
def webhook_view(request: HttpRequest) -> HttpResponse:
    # Telegram secret token tekshiruvi
    expected = getattr(settings, 'TELEGRAM_WEBHOOK_SECRET', '') or ''
    if expected:
        provided = request.headers.get('X-Telegram-Bot-Api-Secret-Token', '')
        if provided != expected:
            return JsonResponse({'ok': False, 'error': 'invalid secret'}, status=403)

    try:
        payload = json.loads(request.body.decode('utf-8') or '{}')
    except json.JSONDecodeError:
        return JsonResponse({'ok': False, 'error': 'invalid json'}, status=400)

    from bot.bot import build_bot, build_dispatcher

    bot = build_bot()
    dp = build_dispatcher()
    update = Update.model_validate(payload, context={'bot': bot})

    asyncio.run(dp.feed_update(bot, update))
    return JsonResponse({'ok': True})
