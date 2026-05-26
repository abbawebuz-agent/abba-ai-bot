"""
Unfold Admin dashboard callback — JIP GROUP
"""
from django.db.models import Count, Sum
from django.utils import timezone
from datetime import timedelta


def dashboard_callback(request, context):
    """
    Unfold dashboard da statistika ko'rsatadi.
    """
    try:
        from core.models import TelegramUser, QRCodeBatch, GiftRedemption, QRCode

        today = timezone.now().date()
        month_start = today.replace(day=1)

        # Asosiy statistika
        total_users = TelegramUser.objects.count()
        active_batches = QRCodeBatch.objects.filter(status='active').count()
        total_scans = QRCode.objects.filter(is_used=True).count()
        pending_gifts = GiftRedemption.objects.filter(status='pending').count()

        context.update({
            "kpi": [
                {
                    "title": "Jami foydalanuvchilar",
                    "metric": str(total_users),
                    "footer": "Telegram orqali ro'yxatdan o'tganlar",
                },
                {
                    "title": "Faol partiyalar",
                    "metric": str(active_batches),
                    "footer": "Hozirda faol partiyalar soni",
                },
                {
                    "title": "Jami skanlar",
                    "metric": str(total_scans),
                    "footer": "Ishlatilgan QR kodlar",
                },
                {
                    "title": "Kutilayotgan sovg'alar",
                    "metric": str(pending_gifts),
                    "footer": "Tasdiqlash kutilmoqda",
                },
            ],
        })
    except Exception:
        pass  # DB tayyor bo'lmasa — xato ko'rsatmasin

    return context
