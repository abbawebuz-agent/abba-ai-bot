from rest_framework import serializers
from core.models import TelegramUser, QRCodeBatch


class UserSerializer(serializers.ModelSerializer):
    region_name = serializers.SerializerMethodField()
    district_name = serializers.SerializerMethodField()

    class Meta:
        model = TelegramUser
        fields = [
            'id',
            'telegram_id',
            'username',
            'first_name',
            'last_name',
            'phone_number',
            'user_type',
            'seller_approved',
            'seller_approved_at',
            'language',
            'region_name',
            'district_name',
            'is_active',
            'created_at',
            'points',
        ]

    def get_region_name(self, obj):
        return obj.region.name_uz if obj.region_id else ''

    def get_district_name(self, obj):
        return obj.district.name_uz if obj.district_id else ''


class QRBatchSerializer(serializers.ModelSerializer):
    store_name = serializers.SerializerMethodField()
    total_codes = serializers.SerializerMethodField()
    activated_count = serializers.SerializerMethodField()

    class Meta:
        model = QRCodeBatch
        fields = [
            'id',
            'name',
            'total_codes',
            'activated_count',
            'store_name',
            'created_at',
            'status',
        ]

    def get_store_name(self, obj):
        return obj.store.name if obj.store_id else ''

    def get_total_codes(self, obj):
        return obj.quantity

    def get_activated_count(self, obj):
        return obj.qr_codes.filter(is_scanned=True).count()
