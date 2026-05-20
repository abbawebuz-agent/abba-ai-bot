"""
Web App backend — TZ §7.4.

Endpoint'lar:
  GET  /api/webapp/me
  GET  /api/webapp/santenik/gifts
  POST /api/webapp/santenik/redemptions
  GET  /api/webapp/santenik/orders
  POST /api/webapp/santenik/orders/<id>/confirm
  POST /api/webapp/santenik/orders/<id>/cancel
  GET  /api/webapp/santenik/leaderboard
  POST /api/webapp/santenik/promo-code
  GET  /api/webapp/seller/dashboard
  GET  /api/webapp/seller/transactions
  GET  /api/webapp/seller/batches
  GET  /api/webapp/seller/batches/<id>
  GET  /api/promotions/
  GET  /api/livestreams/
"""
from __future__ import annotations

import json
from datetime import date, timedelta
from functools import wraps

from django.conf import settings
from django.db import transaction
from django.db.models import Count, Q, Sum
from django.http import HttpRequest, JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

from core.models import (
    Gift,
    GiftRedemption,
    LiveStream,
    Promotion,
    QRCodeBatch,
    SellerPointsTransaction,
    Store,
    TelegramUser,
)
from core.webapp_auth import get_telegram_user_from_request


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _json_body(request: HttpRequest) -> dict:
    if not request.body:
        return {}
    try:
        return json.loads(request.body.decode('utf-8'))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return {}


def webapp_auth_required(role: str | None = None):
    """initData tekshiradi va TelegramUser ni request.tg_user ga qo'yadi."""
    def decorator(view):
        @wraps(view)
        def wrapper(request: HttpRequest, *args, **kwargs):
            parsed = get_telegram_user_from_request(request)
            if not parsed or 'user' not in parsed:
                return JsonResponse({'error': 'unauthorised'}, status=401)
            telegram_id = parsed['user'].get('id')
            if not telegram_id:
                return JsonResponse({'error': 'unauthorised'}, status=401)
            try:
                user = TelegramUser.objects.get(telegram_id=telegram_id)
            except TelegramUser.DoesNotExist:
                return JsonResponse({'error': 'user_not_found'}, status=404)
            if role and user.user_type != role:
                return JsonResponse({'error': 'forbidden', 'role_required': role}, status=403)
            request.tg_user = user
            return view(request, *args, **kwargs)
        return wrapper
    return decorator


def _gift_to_dict(gift: Gift, lang: str = 'uz_latin') -> dict:
    return {
        'id': gift.pk,
        'name': gift.name_ru if lang == 'ru' and gift.name_ru else gift.name_uz_latin,
        'description': (
            gift.description_ru if lang == 'ru' and gift.description_ru else gift.description_uz_latin
        ),
        'image': gift.image.url if gift.image else None,
        'points_cost': gift.points_cost,
        'stock_quantity': gift.stock_quantity,
        'is_active': gift.is_active,
    }


def _redemption_to_dict(r: GiftRedemption, lang: str = 'uz_latin') -> dict:
    return {
        'id': r.pk,
        'gift': _gift_to_dict(r.gift, lang),
        'status': r.status,
        'status_display': r.get_status_display(),
        'requested_at': r.requested_at.isoformat() if r.requested_at else None,
        'user_confirmed': r.user_confirmed,
    }


# ---------------------------------------------------------------------------
# /api/webapp/me
# ---------------------------------------------------------------------------

@require_GET
@webapp_auth_required()
def me(request: HttpRequest) -> JsonResponse:
    u: TelegramUser = request.tg_user
    return JsonResponse({
        'id': u.pk,
        'telegram_id': u.telegram_id,
        'full_name': u.full_name,
        'phone_number': u.phone_number,
        'user_type': u.user_type,
        'language': u.language,
        'points': u.calculate_points(),
        'region': u.region.name_uz if u.region else None,
        'district': u.district.name_uz if u.district else None,
    })


# ---------------------------------------------------------------------------
# Santenik — gifts + orders
# ---------------------------------------------------------------------------

@require_GET
@webapp_auth_required(role=TelegramUser.USER_TYPE_SANTENIK)
def santenik_gifts(request: HttpRequest) -> JsonResponse:
    lang = request.tg_user.language or 'uz_latin'
    qs = Gift.objects.filter(is_active=True).order_by('order', 'points_cost')
    return JsonResponse({'items': [_gift_to_dict(g, lang) for g in qs]})


@csrf_exempt
@require_POST
@webapp_auth_required(role=TelegramUser.USER_TYPE_SANTENIK)
def santenik_create_redemption(request: HttpRequest) -> JsonResponse:
    body = _json_body(request)
    gift_id = body.get('gift_id')
    user: TelegramUser = request.tg_user
    lang = user.language or 'uz_latin'

    try:
        gift = Gift.objects.get(pk=gift_id, is_active=True)
    except (Gift.DoesNotExist, ValueError, TypeError):
        return JsonResponse({'error': 'gift_not_found'}, status=404)

    balance = user.calculate_points(force=True)
    if balance < gift.points_cost:
        return JsonResponse({
            'error': 'insufficient_points',
            'needed': gift.points_cost - balance,
            'balance': balance,
        }, status=400)

    if gift.stock_quantity is not None and gift.stock_quantity <= 0:
        return JsonResponse({'error': 'out_of_stock'}, status=400)

    with transaction.atomic():
        r = GiftRedemption.objects.create(user=user, gift=gift)
        if gift.stock_quantity is not None:
            Gift.objects.filter(pk=gift.pk).update(stock_quantity=gift.stock_quantity - 1)
        user.invalidate_points_cache()

    return JsonResponse({
        'redemption': _redemption_to_dict(r, lang),
        'new_balance': user.calculate_points(force=True),
    }, status=201)


@require_GET
@webapp_auth_required(role=TelegramUser.USER_TYPE_SANTENIK)
def santenik_orders(request: HttpRequest) -> JsonResponse:
    user: TelegramUser = request.tg_user
    lang = user.language or 'uz_latin'
    status_filter = request.GET.get('status')
    qs = GiftRedemption.objects.filter(user=user).select_related('gift').order_by('-requested_at')
    if status_filter:
        qs = qs.filter(status=status_filter)
    return JsonResponse({'items': [_redemption_to_dict(r, lang) for r in qs[:100]]})


@csrf_exempt
@require_POST
@webapp_auth_required(role=TelegramUser.USER_TYPE_SANTENIK)
def santenik_confirm_order(request: HttpRequest, order_id: int) -> JsonResponse:
    try:
        r = GiftRedemption.objects.get(pk=order_id, user=request.tg_user)
    except GiftRedemption.DoesNotExist:
        return JsonResponse({'error': 'order_not_found'}, status=404)
    if r.status != GiftRedemption.STATUS_COMPLETED:
        return JsonResponse({'error': 'invalid_status'}, status=400)
    r.user_confirmed = True
    r.confirmed_at = timezone.now()
    r.save(update_fields=['user_confirmed', 'confirmed_at'])
    return JsonResponse({'ok': True})


@csrf_exempt
@require_POST
@webapp_auth_required(role=TelegramUser.USER_TYPE_SANTENIK)
def santenik_cancel_order(request: HttpRequest, order_id: int) -> JsonResponse:
    try:
        r = GiftRedemption.objects.get(pk=order_id, user=request.tg_user)
    except GiftRedemption.DoesNotExist:
        return JsonResponse({'error': 'order_not_found'}, status=404)
    if r.status not in (GiftRedemption.STATUS_PENDING, GiftRedemption.STATUS_APPROVED):
        return JsonResponse({'error': 'cannot_cancel'}, status=400)
    with transaction.atomic():
        r.status = GiftRedemption.STATUS_CANCELLED_BY_USER
        r.save(update_fields=['status'])
        if r.gift.stock_quantity is not None:
            Gift.objects.filter(pk=r.gift.pk).update(stock_quantity=r.gift.stock_quantity + 1)
        request.tg_user.invalidate_points_cache()
    return JsonResponse({'ok': True, 'new_balance': request.tg_user.calculate_points(force=True)})


@require_GET
@webapp_auth_required(role=TelegramUser.USER_TYPE_SANTENIK)
def santenik_leaderboard(request: HttpRequest) -> JsonResponse:
    period = request.GET.get('period', 'all')
    qs = TelegramUser.objects.filter(user_type=TelegramUser.USER_TYPE_SANTENIK)

    if period == 'month':
        start = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        qs = qs.annotate(
            period_points=Sum('scanned_qrcodes__points', filter=Q(scanned_qrcodes__scanned_at__gte=start)),
        ).order_by('-period_points')
    elif period == 'year':
        start = timezone.now().replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        qs = qs.annotate(
            period_points=Sum('scanned_qrcodes__points', filter=Q(scanned_qrcodes__scanned_at__gte=start)),
        ).order_by('-period_points')
    else:
        qs = qs.order_by('-points')

    items = []
    for u in qs[:10]:
        items.append({
            'name': u.full_name or u.username or '—',
            'points': getattr(u, 'period_points', None) or u.points,
            'region': u.region.name_uz if u.region else None,
        })
    return JsonResponse({'items': items, 'period': period})


@csrf_exempt
@require_POST
@webapp_auth_required(role=TelegramUser.USER_TYPE_SANTENIK)
def santenik_promo_code(request: HttpRequest) -> JsonResponse:
    """Web App orqali QR kod aktivatsiya."""
    from bot.services import _scan_qr_code_sync

    body = _json_body(request)
    code = (body.get('code') or '').strip()
    if not code:
        return JsonResponse({'error': 'code_required'}, status=400)

    with transaction.atomic():
        result = _scan_qr_code_sync(request.tg_user.pk, code, source='webapp')

    response = {'status': result.status}
    if result.status == 'success':
        response.update({
            'points_added': result.points,
            'new_balance': result.balance,
            'store_name': result.store_name,
        })
    elif result.status == 'blocked' and result.blocked_until:
        response['blocked_until'] = result.blocked_until.isoformat()

    return JsonResponse(response)


# ---------------------------------------------------------------------------
# Sotuvchi — dashboard + transactions + batches
# ---------------------------------------------------------------------------

@require_GET
@webapp_auth_required(role=TelegramUser.USER_TYPE_SOTUVCHI)
def seller_dashboard(request: HttpRequest) -> JsonResponse:
    user: TelegramUser = request.tg_user
    stores = list(Store.objects.filter(owner=user).select_related('region'))
    store = stores[0] if stores else None

    transactions = SellerPointsTransaction.objects.filter(seller=user)
    month_start = date.today().replace(day=1)
    month_total = transactions.filter(created_at__date__gte=month_start).aggregate(s=Sum('points'))['s'] or 0
    total_balance = user.calculate_points(force=True)

    cards = {
        'total': 0,
        'scanned': 0,
        'pending': 0,
    }
    if store:
        cards['total'] = store.qr_codes.count()
        cards['scanned'] = store.qr_codes.filter(is_scanned=True).count()
        cards['pending'] = cards['total'] - cards['scanned']

    return JsonResponse({
        'store': {
            'id': store.pk if store else None,
            'name': store.name if store else None,
            'address': store.address if store else None,
            'commission_percent': str(store.commission_percent) if store else None,
        },
        'balance': total_balance,
        'month_points': month_total,
        'cards': cards,
    })


@require_GET
@webapp_auth_required(role=TelegramUser.USER_TYPE_SOTUVCHI)
def seller_transactions(request: HttpRequest) -> JsonResponse:
    user: TelegramUser = request.tg_user
    qs = (
        SellerPointsTransaction.objects.filter(seller=user)
        .select_related('store')
        .order_by('-created_at')[:200]
    )
    items = []
    for tx in qs:
        items.append({
            'id': tx.pk,
            'type': tx.transaction_type,
            'type_display': tx.get_transaction_type_display(),
            'points': tx.points,
            'sales_amount_usd': str(tx.sales_amount_usd) if tx.sales_amount_usd else None,
            'note': tx.note,
            'period_start': tx.period_start.isoformat() if tx.period_start else None,
            'period_end': tx.period_end.isoformat() if tx.period_end else None,
            'created_at': tx.created_at.isoformat(),
        })
    return JsonResponse({'items': items})


@require_GET
@webapp_auth_required(role=TelegramUser.USER_TYPE_SOTUVCHI)
def seller_batches(request: HttpRequest) -> JsonResponse:
    user: TelegramUser = request.tg_user
    qs = (
        QRCodeBatch.objects.filter(store__owner=user)
        .annotate(scanned=Count('qr_codes', filter=Q(qr_codes__is_scanned=True)))
        .order_by('-created_at')
    )
    items = []
    for b in qs:
        items.append({
            'id': b.pk,
            'name': b.name,
            'quantity': b.quantity,
            'points_per_code': b.points_per_code,
            'scanned': b.scanned,
            'activation_rate': round((b.scanned / b.quantity * 100) if b.quantity else 0, 1),
            'status': b.status,
            'delivery_status': b.delivery_status,
            'created_at': b.created_at.isoformat(),
        })
    return JsonResponse({'items': items})


@require_GET
@webapp_auth_required(role=TelegramUser.USER_TYPE_SOTUVCHI)
def seller_batch_detail(request: HttpRequest, batch_id: int) -> JsonResponse:
    try:
        b = QRCodeBatch.objects.select_related('store').get(pk=batch_id, store__owner=request.tg_user)
    except QRCodeBatch.DoesNotExist:
        return JsonResponse({'error': 'batch_not_found'}, status=404)
    codes = []
    for qr in b.qr_codes.select_related('scanned_by').order_by('serial_number')[:1000]:
        codes.append({
            'serial': qr.serial_number,
            'is_scanned': qr.is_scanned,
            'scanned_at': qr.scanned_at.isoformat() if qr.scanned_at else None,
            'scanned_by_name': qr.scanned_by.full_name if qr.scanned_by else None,
            'points': qr.points,
        })
    return JsonResponse({
        'id': b.pk,
        'name': b.name,
        'quantity': b.quantity,
        'codes': codes,
    })


# ---------------------------------------------------------------------------
# Public — promotions + livestreams
# ---------------------------------------------------------------------------

@require_GET
def promotions(request: HttpRequest) -> JsonResponse:
    now = timezone.now()
    qs = Promotion.objects.filter(is_active=True).filter(
        Q(starts_at__isnull=True) | Q(starts_at__lte=now),
    ).filter(
        Q(ends_at__isnull=True) | Q(ends_at__gte=now),
    ).order_by('order', '-created_at')
    items = [{
        'id': p.pk,
        'title_uz': p.title_uz,
        'title_ru': p.title_ru,
        'text_uz': p.text_uz,
        'text_ru': p.text_ru,
        'image': p.image.url if p.image else None,
        'link': p.link,
    } for p in qs]
    return JsonResponse({'items': items})


@require_GET
def livestreams(request: HttpRequest) -> JsonResponse:
    now = timezone.now()
    horizon = now + timedelta(days=30)
    qs = LiveStream.objects.filter(
        Q(status=LiveStream.STATUS_PLANNED, starts_at__gte=now - timedelta(hours=1), starts_at__lte=horizon)
        | Q(status=LiveStream.STATUS_LIVE),
    ).order_by('starts_at')
    items = [{
        'id': ls.pk,
        'title_uz': ls.title_uz,
        'title_ru': ls.title_ru,
        'stream_url': ls.stream_url,
        'starts_at': ls.starts_at.isoformat(),
        'status': ls.status,
        'cover_image': ls.cover_image.url if ls.cover_image else None,
    } for ls in qs]
    return JsonResponse({'items': items})


# ---------------------------------------------------------------------------
# Template views — Web App HTML page entry
# ---------------------------------------------------------------------------

def webapp_santenik(request: HttpRequest):
    from django.shortcuts import render
    return render(request, 'webapp/index.html')


def webapp_seller(request: HttpRequest):
    from django.shortcuts import render
    return render(request, 'webapp/seller.html')
