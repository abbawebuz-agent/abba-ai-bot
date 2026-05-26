"""
JIP Admin SPA view — serves the Claude Design React SPA
URL: /jip-admin/

Authentication: requires Django staff login (redirects to /admin/login/)
Stats: passes real model counts to the SPA template
"""
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.views.decorators.cache import never_cache


def _get_stats(request):
    """Return real KPI stats for the SPA template."""
    stats = {
        'users_total': 0,
        'users_santenik': 0,
        'users_sotuvchi': 0,
        'batches_total': 0,
        'batches_active': 0,
        'qr_total': 0,
        'qr_scanned': 0,
        'gifts_pending': 0,
        'txns_total': 0,
        'audit_total': 0,
    }
    try:
        from core.models import (
            TelegramUser, QRCodeBatch, QRCode,
            GiftRedemption, SellerPointsTransaction, ActivityLog
        )
        stats['users_total']    = TelegramUser.objects.count()
        stats['users_santenik'] = TelegramUser.objects.filter(user_type='santenik').count()
        stats['users_sotuvchi'] = TelegramUser.objects.filter(user_type='sotuvchi').count()
        stats['batches_total']  = QRCodeBatch.objects.count()
        stats['batches_active'] = QRCodeBatch.objects.filter(status='active').count()
        stats['qr_total']       = QRCode.objects.count()
        stats['qr_scanned']     = QRCode.objects.filter(is_used=True).count()
        stats['gifts_pending']  = GiftRedemption.objects.filter(status='pending').count()
        stats['txns_total']     = SellerPointsTransaction.objects.count()
        try:
            stats['audit_total'] = ActivityLog.objects.count()
        except Exception:
            pass
    except Exception:
        pass  # DB not ready or model import error — use defaults
    return stats


@never_cache
@staff_member_required(login_url='/admin/login/')
def jip_admin_spa(request):
    """Serve the JIP Admin SPA (Claude Design 1:1 implementation)."""
    context = {
        'stats': _get_stats(request),
    }
    return render(request, 'jip_admin/index.html', context)
