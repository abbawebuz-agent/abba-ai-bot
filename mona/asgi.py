"""
ASGI config for mona project.
"""
import os

# MUHIM: Django import qilishdan OLDIN settings module ni o'rnatish kerak!
# Aks holda Django import jarayonida settings izlab topilmaydi → ROOT_URLCONF AttributeError
os.environ.setdefault('DJANGO_SETTINGS_MODULE', os.environ.get('DJANGO_SETTINGS_MODULE', 'mona.settings.production'))

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

django_asgi_app = get_asgi_application()

# ── Avto-backup: har kuni 04:00 (Asia/Tashkent) ──────────────────────────
# Railway'da Celery worker ishlamaydi, shuning uchun backup'ni shu yagona
# uvicorn jarayoni ichida (ASGI lifespan) jadvallaymiz. --workers 1 bo'lgani
# uchun dublikat bo'lmaydi.
import asyncio
import logging
from datetime import datetime, timedelta

_bg_tasks = set()
_blog = logging.getLogger('jip.backup')


async def _daily_backup_loop():
    from django.core.management import call_command
    try:
        from zoneinfo import ZoneInfo
        tz = ZoneInfo('Asia/Tashkent')
    except Exception:
        tz = None
    while True:
        try:
            now = datetime.now(tz)
            nxt = now.replace(hour=4, minute=0, second=0, microsecond=0)
            if nxt <= now:
                nxt += timedelta(days=1)
            wait_s = max(60.0, (nxt - now).total_seconds())
            _blog.info('Keyingi avto-backup: %s (%.0f s)', nxt.isoformat(), wait_s)
            await asyncio.sleep(wait_s)
            loop = asyncio.get_event_loop()
            # 1) SQL dump
            await loop.run_in_executor(None, lambda: call_command('backup_db'))
            _blog.info('Avto-backup (SQL) bajarildi')
            # 2) Excel data eksport — Celery beat Railway'da ishlamaydi,
            #    shuning uchun Excel ham shu loop orqali yuboriladi.
            try:
                await loop.run_in_executor(None, lambda: call_command('backup_excel'))
                _blog.info('Avto-backup (Excel) bajarildi')
            except Exception:
                _blog.exception('Avto-backup (Excel) xato — SQL baribir yuborildi')
        except asyncio.CancelledError:
            raise
        except Exception:
            _blog.exception('Avto-backup xato — 1 soatdan keyin qayta urinish')
            await asyncio.sleep(3600)


async def lifespan_app(scope, receive, send):
    while True:
        message = await receive()
        if message['type'] == 'lifespan.startup':
            try:
                t = asyncio.ensure_future(_daily_backup_loop())
                _bg_tasks.add(t)
                t.add_done_callback(_bg_tasks.discard)
            except Exception:
                _blog.exception('Avto-backup loop ishga tushmadi')
            await send({'type': 'lifespan.startup.complete'})
        elif message['type'] == 'lifespan.shutdown':
            for t in list(_bg_tasks):
                t.cancel()
            await send({'type': 'lifespan.shutdown.complete'})
            return


application = ProtocolTypeRouter({
    "lifespan": lifespan_app,
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter([
            # Add WebSocket URL routing here if needed
        ])
    ),
})

