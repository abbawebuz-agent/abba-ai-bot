"""
URL configuration for core app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TelegramUserViewSet, QRCodeViewSet, GiftViewSet
from .webapp_views import (
    webapp_view, get_user_data, get_gifts,
    get_user_redemptions, request_gift, confirm_delivery, cancel_order, get_translations, get_qr_history,
    get_promotions, register_qr_code, get_promotion_detail, get_privacy_policy, update_user_language,
    get_admin_contact, resend_registration_step,
    get_live_streams, get_live_stream_detail, get_top_users,
    seller_webapp_view, seller_dashboard, seller_transactions, seller_batches,
    seller_balance_history, seller_batch_qr_detail, seller_top_santexniks, seller_commission_calc,
)

router = DefaultRouter()
router.register(r'users', TelegramUserViewSet, basename='user')
router.register(r'qrcodes', QRCodeViewSet, basename='qrcode')
router.register(r'gifts', GiftViewSet, basename='gift')

urlpatterns = [
    path('', include(router.urls)),
    # Web App endpoints
    path('webapp/', webapp_view, name='webapp'),
    path('webapp/user/', get_user_data, name='webapp_user'),
    path('webapp/translations/', get_translations, name='webapp_translations'),
    path('webapp/gifts/', get_gifts, name='webapp_gifts'),
    path('webapp/redemptions/', get_user_redemptions, name='webapp_redemptions'),
    path('webapp/request-gift/', request_gift, name='webapp_request_gift'),
    path('webapp/confirm-delivery/', confirm_delivery, name='webapp_confirm_delivery'),
    path('webapp/cancel-order/', cancel_order, name='webapp_cancel_order'),
    path('webapp/qr-history/', get_qr_history, name='webapp_qr_history'),
    path('webapp/promotions/', get_promotions, name='webapp_promotions'),
    path('webapp/promotions/<int:promotion_id>/', get_promotion_detail, name='webapp_promotion_detail'),
    path('webapp/register-qr/', register_qr_code, name='webapp_register_qr'),
    path('webapp/privacy-policy/', get_privacy_policy, name='webapp_privacy_policy'),
    path('webapp/update-language/', update_user_language, name='webapp_update_language'),
    path('webapp/admin-contact/', get_admin_contact, name='webapp_admin_contact'),
    path('webapp/resend-registration-step/', resend_registration_step, name='webapp_resend_registration_step'),
    path('webapp/live-streams/', get_live_streams, name='webapp_live_streams'),
    path('webapp/live-streams/<int:stream_id>/', get_live_stream_detail, name='webapp_live_stream_detail'),
    path('webapp/top-users/', get_top_users, name='webapp_top_users'),
    # Seller Web App — tiklandi (bot hali WebApp tugmasini ko'rsatadi)
    path('webapp/seller/', seller_webapp_view, name='webapp_seller'),
    path('webapp/seller/dashboard/', seller_dashboard, name='webapp_seller_dashboard'),
    path('webapp/seller/transactions/', seller_transactions, name='webapp_seller_transactions'),
    path('webapp/seller/batches/', seller_batches, name='webapp_seller_batches'),
    path('webapp/seller/balance-history/', seller_balance_history, name='webapp_seller_balance_history'),
    path('webapp/seller/batch/<int:batch_id>/qr/', seller_batch_qr_detail, name='webapp_seller_batch_qr'),
    path('webapp/seller/top-santexniks/', seller_top_santexniks, name='webapp_seller_top_santexniks'),
    path('webapp/seller/commission-calc/', seller_commission_calc, name='webapp_seller_commission_calc'),
]

