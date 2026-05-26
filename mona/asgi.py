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

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter([
            # Add WebSocket URL routing here if needed
        ])
    ),
})

