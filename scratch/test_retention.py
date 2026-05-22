import os
import django
from datetime import date, timedelta
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mona.settings')
django.setup()

from core.models import TelegramUser, QRCode, PromoCodeAttempt, GiftRedemption
from core.dashboard_stats import compute_dashboard_charts

def test_retention():
    date_to = timezone.now().date()
    date_from = date_to - timedelta(days=7)
    
    print(f"Testing retention for period: {date_from} to {date_to}")
    
    charts = compute_dashboard_charts(date_from, date_to)
    retention = charts.get('retention', {})
    
    print(f"New Users: {retention.get('new_users')}")
    print(f"Returning Users: {retention.get('returning_users')}")
    print(f"Total Active: {retention.get('total_active')}")
    
    # Check manual counts
    new_users = TelegramUser.objects.filter(created_at__date__range=(date_from, date_to)).count()
    print(f"Manual New Users Count: {new_users}")
    
    # Check returning
    active_old = set()
    active_old.update(QRCode.objects.filter(
        scanned_at__sdate__range=(date_from, date_to),
        scanned_by__created_at__date__lt=date_from
    ).values_list('scanned_by_id', flat=True))
    
    print(f"Manual Returning Users Count: {len(active_old)}")

if __name__ == "__main__":
    test_retention()
