"""Activity log signal handlers.

Tracks:
- Admin login / logout / login failed
- Model create/update/delete (faqat MUHIM modellar)
"""
import threading

from django.contrib.auth.signals import (
    user_logged_in, user_logged_out, user_login_failed,
)
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import (
    ActivityLog,
    QRCodeBatch,
    SellerPointsTransaction,
    GiftRedemption,
    Gift,
    SellerRegistrationCode,
    TelegramUser,
    log_event,
)


# ──────────────────────────────────────────────────────────────────
# Request context (current request stored in thread-local)
# ──────────────────────────────────────────────────────────────────
_request_local = threading.local()


def set_current_request(request):
    _request_local.request = request


def get_current_request():
    return getattr(_request_local, 'request', None)


# ──────────────────────────────────────────────────────────────────
# Login / Logout / Failed login
# ──────────────────────────────────────────────────────────────────
@receiver(user_logged_in)
def on_login(sender, request, user, **kwargs):
    log_event(
        action_type=ActivityLog.ACTION_LOGIN,
        user=user,
        description=f"{user.username} admin paneliga kirdi",
        request=request,
    )


@receiver(user_logged_out)
def on_logout(sender, request, user, **kwargs):
    if user:
        log_event(
            action_type=ActivityLog.ACTION_LOGOUT,
            user=user,
            description=f"{user.username} chiqdi",
            request=request,
        )


@receiver(user_login_failed)
def on_login_failed(sender, credentials, request=None, **kwargs):
    username = credentials.get('username', 'unknown')
    log_event(
        action_type=ActivityLog.ACTION_LOGIN_FAILED,
        description=f"❌ Login xato: {username}",
        request=request,
        attempted_username=username,
    )


# ──────────────────────────────────────────────────────────────────
# Model create/update — faqat muhim modellar
# ──────────────────────────────────────────────────────────────────
TRACKED_MODELS = [
    QRCodeBatch,
    SellerPointsTransaction,
    GiftRedemption,
    Gift,
    SellerRegistrationCode,
]


def _make_save_handler(model_cls):
    @receiver(post_save, sender=model_cls, weak=False)
    def _handler(sender, instance, created, **kwargs):
        # ActivityLog ni o'zini logga yozish — infinite loop
        if isinstance(instance, ActivityLog):
            return
        try:
            request = get_current_request()
            user = getattr(request, 'user', None) if request else None
            action = ActivityLog.ACTION_CREATE if created else ActivityLog.ACTION_UPDATE
            verb = 'yaratdi' if created else 'yangiladi'
            log_event(
                action_type=action,
                user=user if (user and getattr(user, 'is_authenticated', False)) else None,
                target=instance,
                description=f"{type(instance).__name__} {verb}: {str(instance)[:120]}",
                request=request,
            )
        except Exception:
            import logging
            logging.getLogger(__name__).exception('post_save signal failed')
    return _handler


def _make_delete_handler(model_cls):
    @receiver(post_delete, sender=model_cls, weak=False)
    def _handler(sender, instance, **kwargs):
        if isinstance(instance, ActivityLog):
            return
        try:
            request = get_current_request()
            user = getattr(request, 'user', None) if request else None
            log_event(
                action_type=ActivityLog.ACTION_DELETE,
                user=user if (user and getattr(user, 'is_authenticated', False)) else None,
                target=instance,
                description=f"{type(instance).__name__} o'chirildi: {str(instance)[:120]}",
                request=request,
            )
        except Exception:
            import logging
            logging.getLogger(__name__).exception('post_delete signal failed')
    return _handler


# Bind signals for each tracked model
_handlers = []
for _cls in TRACKED_MODELS:
    _handlers.append(_make_save_handler(_cls))
    _handlers.append(_make_delete_handler(_cls))
