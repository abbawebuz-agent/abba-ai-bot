from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta
from core.models import TelegramUser, QRCodeBatch, QRCode
from .serializers import UserSerializer, QRBatchSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['username'] = self.user.username
        data['is_superuser'] = self.user.is_superuser
        return data


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_stats(request):
    now = timezone.now()
    today = now.date()
    week_ago = now - timedelta(days=7)
    month_ago = now - timedelta(days=30)

    total_users = TelegramUser.objects.count()
    santeniklar = TelegramUser.objects.filter(user_type='santenik').count()
    sotuvchilar = TelegramUser.objects.filter(user_type='sotuvchi', seller_approved=True).count()
    pending_sellers = TelegramUser.objects.filter(user_type='sotuvchi', seller_approved=False).count()

    total_qr = QRCode.objects.count()
    activated_qr = QRCode.objects.filter(is_scanned=True).count()
    today_scans = QRCode.objects.filter(scanned_at__date=today, is_scanned=True).count()
    week_scans = QRCode.objects.filter(scanned_at__gte=week_ago, is_scanned=True).count()

    # Last 7 days scans chart
    scans_chart = []
    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        count = QRCode.objects.filter(scanned_at__date=day, is_scanned=True).count()
        scans_chart.append({'date': str(day), 'scans': count})

    # Last 30 days user registrations
    users_chart = []
    for i in range(29, -1, -1):
        day = today - timedelta(days=i)
        count = TelegramUser.objects.filter(created_at__date=day).count()
        users_chart.append({'date': str(day), 'users': count})

    active_batches = QRCodeBatch.objects.count()

    return Response({
        'total_users': total_users,
        'santeniklar': santeniklar,
        'sotuvchilar': sotuvchilar,
        'pending_sellers': pending_sellers,
        'total_qr': total_qr,
        'activated_qr': activated_qr,
        'today_scans': today_scans,
        'week_scans': week_scans,
        'active_batches': active_batches,
        'scans_chart': scans_chart,
        'users_chart': users_chart,
    })


class UserListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = TelegramUser.objects.select_related('region', 'district').order_by('-created_at')
        user_type = self.request.query_params.get('user_type')
        search = self.request.query_params.get('search')
        approved = self.request.query_params.get('seller_approved')
        if user_type:
            qs = qs.filter(user_type=user_type)
        if search:
            qs = qs.filter(
                Q(first_name__icontains=search) |
                Q(username__icontains=search) |
                Q(phone_number__icontains=search)
            )
        if approved == 'false':
            qs = qs.filter(user_type='sotuvchi', seller_approved=False)
        elif approved == 'true':
            qs = qs.filter(seller_approved=True)
        return qs


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    queryset = TelegramUser.objects.all()


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def approve_seller(request, pk):
    try:
        user = TelegramUser.objects.get(pk=pk)
        user.seller_approved = True
        user.seller_approved_at = timezone.now()
        user.save(update_fields=['seller_approved', 'seller_approved_at'])
        _notify_seller(user, approved=True)
        return Response({'status': 'approved'})
    except TelegramUser.DoesNotExist:
        return Response({'error': 'Not found'}, status=404)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reject_seller(request, pk):
    try:
        user = TelegramUser.objects.get(pk=pk)
        user.seller_approved = False
        user.save(update_fields=['seller_approved'])
        _notify_seller(user, approved=False)
        return Response({'status': 'rejected'})
    except TelegramUser.DoesNotExist:
        return Response({'error': 'Not found'}, status=404)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def bulk_delete_users(request):
    ids = request.data.get('ids', [])
    deleted, _ = TelegramUser.objects.filter(id__in=ids).delete()
    return Response({'deleted': deleted})


class QRBatchListView(generics.ListAPIView):
    serializer_class = QRBatchSerializer
    permission_classes = [IsAuthenticated]
    queryset = QRCodeBatch.objects.select_related('store').annotate(
        _activated=Count('qr_codes', filter=Q(qr_codes__is_scanned=True))
    ).order_by('-created_at')


def _notify_seller(user, approved: bool):
    import threading
    import urllib.request
    import json as _json
    from django.conf import settings

    token = getattr(settings, 'TELEGRAM_BOT_TOKEN', '')
    if not token or not user.telegram_id:
        return
    text = (
        '✅ Arizangiz tasdiqlandi! Endi botdan foydalanishingiz mumkin.'
        if approved else
        '❌ Arizangiz rad etildi. Murojaat: @jip_admin'
    )

    def _send():
        try:
            data = _json.dumps({'chat_id': user.telegram_id, 'text': text}).encode()
            req = urllib.request.Request(
                f'https://api.telegram.org/bot{token}/sendMessage',
                data=data,
                headers={'Content-Type': 'application/json'},
                method='POST',
            )
            urllib.request.urlopen(req, timeout=5)
        except Exception:
            pass

    threading.Thread(target=_send, daemon=True).start()
