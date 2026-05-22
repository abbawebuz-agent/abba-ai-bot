"""Django async view — Telegram webhook updates qabul qilish."""
import json
import logging
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.conf import settings

logger = logging.getLogger(__name__)

_bot = None
_dp = None


def _get_bot_dp():
    global _bot, _dp
    if _bot is None:
        from bot.bot import bot, dp
        _bot = bot
        _dp = dp
    return _bot, _dp


@csrf_exempt
async def telegram_webhook_view(request, token):
    if token != settings.TELEGRAM_BOT_TOKEN:
        return HttpResponse(status=403)
    if request.method != 'POST':
        return HttpResponse(status=405)
    try:
        from aiogram.types import Update
        bot, dp = _get_bot_dp()
        data = json.loads(request.body)
        update = Update.model_validate(data)
        await dp.feed_update(bot, update)
    except Exception as e:
        logger.error(f'Webhook error: {e}', exc_info=True)
    return HttpResponse('ok')
