from django.http import JsonResponse
from django.urls import path

from . import webapp_views as wa

app_name = 'core'


def health(_request):
    return JsonResponse({'status': 'ok'})


def index(_request):
    return JsonResponse({
        'service': 'JIP Loyalty Platform',
        'status': 'running',
        'phase': 'Faza 1–5 complete',
    })


urlpatterns = [
    path('', index, name='index'),
    path('health/', health, name='health'),

    # Web App HTML
    path('webapp/', wa.webapp_santenik, name='webapp_santenik'),
    path('webapp/seller/', wa.webapp_seller, name='webapp_seller'),

    # Web App API — common
    path('api/webapp/me', wa.me, name='api_me'),
    path('api/promotions/', wa.promotions, name='api_promotions'),
    path('api/livestreams/', wa.livestreams, name='api_livestreams'),

    # Santenik API
    path('api/webapp/santenik/gifts', wa.santenik_gifts, name='api_santenik_gifts'),
    path('api/webapp/santenik/redemptions', wa.santenik_create_redemption, name='api_santenik_redeem'),
    path('api/webapp/santenik/orders', wa.santenik_orders, name='api_santenik_orders'),
    path('api/webapp/santenik/orders/<int:order_id>/confirm', wa.santenik_confirm_order, name='api_santenik_confirm'),
    path('api/webapp/santenik/orders/<int:order_id>/cancel', wa.santenik_cancel_order, name='api_santenik_cancel'),
    path('api/webapp/santenik/leaderboard', wa.santenik_leaderboard, name='api_santenik_leaderboard'),
    path('api/webapp/santenik/promo-code', wa.santenik_promo_code, name='api_santenik_promo'),

    # Sotuvchi API
    path('api/webapp/seller/dashboard', wa.seller_dashboard, name='api_seller_dashboard'),
    path('api/webapp/seller/transactions', wa.seller_transactions, name='api_seller_transactions'),
    path('api/webapp/seller/batches', wa.seller_batches, name='api_seller_batches'),
    path('api/webapp/seller/batches/<int:batch_id>', wa.seller_batch_detail, name='api_seller_batch'),
]
