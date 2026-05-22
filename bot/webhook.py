"""
Webhook configuration for Telegram bot in production.
"""
import os
import logging
import django
from aiogram import Bot, Dispatcher
from aiogram.webhook.aiohttp_server import SimpleRequestHandler
from aiohttp import web

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mona.settings')
django.setup()

from django.conf import settings
from .bot import dp, bot

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


async def on_startup(bot: Bot):
    """
    Выполняется при запуске webhook-сервера.

    Webhook ставим только если он ещё не установлен на нужный URL —
    избегаем лишних setWebhook на каждом рестарте. drop_pending_updates=False
    гарантирует, что обновления, накопившиеся во время деплоя, не потеряются.
    """
    desired_url = f"{settings.WEBHOOK_URL}/webhook/{settings.TELEGRAM_BOT_TOKEN}"

    try:
        info = await bot.get_webhook_info()
        if info and info.url == desired_url:
            logger.info(f"Webhook уже установлен: {desired_url} (skip setWebhook)")
            return

        await bot.set_webhook(
            url=desired_url,
            allowed_updates=["message", "callback_query"],
            drop_pending_updates=False,
        )
        logger.info(f"Webhook установлен: {desired_url}")
    except Exception as e:
        logger.error(f"Ошибка при установке webhook: {e}")


# on_shutdown намеренно не определён и не регистрируется: webhook должен
# оставаться зарегистрированным в Telegram при `docker compose down`/деплое.
# Если delete_webhook вызвать — на время даунтайма Telegram перестанет
# складывать апдейты, и они потеряются. Сейчас Telegram держит апдейты
# в очереди до 24 часов до возврата сервиса.


def create_webhook_app():
    """Создает aiohttp приложение для webhook."""
    app = web.Application()

    # Создаем обработчик webhook
    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
    )

    # Регистрируем путь для webhook
    webhook_path = f"/webhook/{settings.TELEGRAM_BOT_TOKEN}"
    webhook_requests_handler.register(app, path=webhook_path)

    # Только startup. Shutdown не трогает webhook (см. комментарий выше).
    app.on_startup.append(lambda app: on_startup(bot))

    return app


async def health_check(request):
    """Health check endpoint."""
    return web.json_response({"status": "ok"})


def get_webhook_app():
    """Возвращает настроенное приложение для webhook."""
    app = create_webhook_app()
    
    # Добавляем health check
    app.router.add_get("/health", health_check)
    
    return app

