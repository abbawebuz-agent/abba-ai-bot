"""
JIP admin panel.

Hozir minimal ModelAdmin'lar — Faza 4'da kengaytiriladi (per-store dashboard,
batch generatsiya formasi, sotuvchiga ball qo'shish formasi va h.k.).
"""
from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from .models import (
    AdminContactSettings,
    BroadcastMessage,
    Gift,
    GiftRedemption,
    LiveStream,
    LiveStreamWinner,
    MonthlyPromoTicket,
    MonthlyReminderLog,
    MonthlyReminderSettings,
    PrivacyPolicy,
    PromoCodeAttempt,
    Promotion,
    QRCode,
    QRCodeBatch,
    QRCodeScanAttempt,
    RegionMessageLog,
    SellerPointsTransaction,
    Store,
    TelegramUser,
    UzDistrict,
    UzRegion,
    VideoInstruction,
)


admin.site.site_header = "JIP — Sodiqlik Dasturi"
admin.site.site_title = "JIP Admin"
admin.site.index_title = "Boshqaruv paneli"


@admin.register(UzRegion)
class UzRegionAdmin(admin.ModelAdmin):
    list_display = ('code', 'name_uz', 'name_ru')
    search_fields = ('code', 'name_uz', 'name_ru')


@admin.register(UzDistrict)
class UzDistrictAdmin(admin.ModelAdmin):
    list_display = ('region', 'code', 'name_uz', 'name_ru')
    list_filter = ('region',)
    search_fields = ('code', 'name_uz', 'name_ru')
    autocomplete_fields = ('region',)


@admin.register(TelegramUser)
class TelegramUserAdmin(SimpleHistoryAdmin):
    list_display = (
        'full_name', 'phone_number', 'user_type', 'region', 'points', 'is_active', 'created_at',
    )
    list_filter = ('user_type', 'language', 'region', 'is_active', 'privacy_accepted')
    search_fields = ('first_name', 'last_name', 'username', 'phone_number', 'telegram_id')
    readonly_fields = ('telegram_id', 'created_at', 'updated_at', 'points')
    autocomplete_fields = ('region', 'district')


@admin.register(Store)
class StoreAdmin(SimpleHistoryAdmin):
    list_display = ('name', 'region', 'district', 'owner', 'phone', 'commission_percent', 'is_active')
    list_filter = ('is_active', 'region', 'district')
    search_fields = ('name', 'legal_name', 'phone', 'owner__first_name', 'owner__last_name')
    autocomplete_fields = ('owner', 'region', 'district')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(QRCodeBatch)
class QRCodeBatchAdmin(SimpleHistoryAdmin):
    list_display = (
        'name', 'store', 'quantity', 'points_per_code',
        'status', 'delivery_status', 'created_at',
    )
    list_filter = ('status', 'delivery_status', 'store')
    search_fields = ('name', 'store__name')
    autocomplete_fields = ('store',)
    readonly_fields = ('status', 'zip_file', 'error_message', 'created_at', 'completed_at', 'created_by')
    actions = ['action_generate_zip', 'action_mark_shipped', 'action_mark_delivered']

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
            if not obj.name:
                from datetime import date
                today = date.today()
                prefix = today.strftime('%b').upper()
                idx = QRCodeBatch.objects.filter(
                    store=obj.store, created_at__year=today.year, created_at__month=today.month,
                ).count() + 1
                obj.name = f"{prefix}-{today.year}-{idx:03d}"
        super().save_model(request, obj, form, change)
        if not change:
            from core.tasks import generate_batch_zip
            generate_batch_zip.delay(obj.pk)

    @admin.action(description="ZIP qayta generatsiya qilish")
    def action_generate_zip(self, request, queryset):
        from core.tasks import generate_batch_zip
        for b in queryset:
            generate_batch_zip.delay(b.pk)
        self.message_user(request, f"{queryset.count()} batch uchun ZIP generatsiya navbatga qo'yildi")

    @admin.action(description="Jo'natildi deb belgilash")
    def action_mark_shipped(self, request, queryset):
        from django.utils import timezone
        queryset.update(delivery_status=QRCodeBatch.DELIVERY_SHIPPED, shipped_at=timezone.now())

    @admin.action(description="Yetkazib berildi deb belgilash")
    def action_mark_delivered(self, request, queryset):
        from django.utils import timezone
        queryset.update(delivery_status=QRCodeBatch.DELIVERY_DELIVERED, delivered_at=timezone.now())


@admin.register(QRCode)
class QRCodeAdmin(SimpleHistoryAdmin):
    list_display = ('serial_number', 'store', 'batch', 'points', 'is_scanned', 'scanned_at', 'scanned_by')
    list_filter = ('is_scanned', 'is_deleted', 'store', 'batch')
    search_fields = ('code', 'hash_code', 'serial_number')
    autocomplete_fields = ('store', 'batch', 'scanned_by')
    readonly_fields = (
        'code', 'hash_code', 'serial_number', 'image_path', 'points',
        'store', 'batch', 'generated_at', 'scanned_at', 'scanned_by', 'is_scanned',
    )


@admin.register(QRCodeScanAttempt)
class QRCodeScanAttemptAdmin(admin.ModelAdmin):
    list_display = ('user', 'qr_code', 'attempted_at', 'is_successful')
    list_filter = ('is_successful',)
    search_fields = ('user__first_name', 'qr_code__code')
    readonly_fields = ('user', 'qr_code', 'attempted_at', 'is_successful')


@admin.register(PromoCodeAttempt)
class PromoCodeAttemptAdmin(admin.ModelAdmin):
    list_display = ('user', 'raw_code', 'source', 'is_successful', 'attempted_at')
    list_filter = ('is_successful', 'source')
    search_fields = ('user__first_name', 'raw_code')
    readonly_fields = ('user', 'raw_code', 'attempted_at', 'is_successful', 'source')


@admin.register(SellerPointsTransaction)
class SellerPointsTransactionAdmin(SimpleHistoryAdmin):
    list_display = (
        'seller', 'store', 'transaction_type', 'points',
        'sales_amount_usd', 'period_start', 'period_end', 'created_at',
    )
    list_filter = ('transaction_type', 'store')
    search_fields = ('seller__first_name', 'seller__last_name', 'note')
    autocomplete_fields = ('seller', 'store')
    readonly_fields = ('created_by', 'created_at')

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
        # Sotuvchi balansini invalidatsiya qilish
        from core.tasks import recalc_user_points
        recalc_user_points.delay(obj.seller_id)


@admin.register(Gift)
class GiftAdmin(SimpleHistoryAdmin):
    list_display = ('name_uz_latin', 'points_cost', 'stock_quantity', 'is_active', 'order')
    list_filter = ('is_active',)
    search_fields = ('name_uz_latin', 'name_ru')


@admin.register(GiftRedemption)
class GiftRedemptionAdmin(SimpleHistoryAdmin):
    list_display = ('user', 'gift', 'status', 'requested_at', 'user_confirmed')
    list_filter = ('status', 'user_confirmed')
    search_fields = ('user__first_name', 'user__last_name', 'gift__name_uz_latin')
    autocomplete_fields = ('user', 'gift')
    readonly_fields = ('requested_at', 'confirmed_at')


@admin.register(MonthlyPromoTicket)
class MonthlyPromoTicketAdmin(admin.ModelAdmin):
    list_display = ('order', 'month', 'user', 'store', 'qr_code', 'scanned_at')
    list_filter = ('month', 'store')
    search_fields = ('user__first_name', 'user__last_name', 'qr_code__code')
    readonly_fields = ('order', 'month', 'qr_code', 'user', 'store', 'scanned_at', 'created_at')


@admin.register(BroadcastMessage)
class BroadcastMessageAdmin(SimpleHistoryAdmin):
    list_display = (
        'title', 'status', 'user_type_filter', 'region_filter', 'store_filter',
        'total_recipients', 'sent_count', 'created_at',
    )
    list_filter = ('status', 'user_type_filter', 'language_filter')
    search_fields = ('title',)
    autocomplete_fields = ('region_filter', 'store_filter')
    readonly_fields = (
        'status', 'started_at', 'finished_at',
        'total_recipients', 'sent_count', 'failed_count',
        'created_by', 'created_at',
    )


@admin.register(RegionMessageLog)
class RegionMessageLogAdmin(admin.ModelAdmin):
    list_display = ('broadcast', 'user', 'sent_at', 'is_successful')
    list_filter = ('is_successful',)
    search_fields = ('user__first_name',)
    readonly_fields = ('broadcast', 'user', 'sent_at', 'is_successful', 'error_message')


@admin.register(Promotion)
class PromotionAdmin(SimpleHistoryAdmin):
    list_display = ('title_uz', 'is_active', 'order', 'starts_at', 'ends_at')
    list_filter = ('is_active',)
    search_fields = ('title_uz', 'title_ru')


@admin.register(PrivacyPolicy)
class PrivacyPolicyAdmin(admin.ModelAdmin):
    list_display = ('version', 'is_active', 'created_at')
    list_filter = ('is_active',)


@admin.register(AdminContactSettings)
class AdminContactSettingsAdmin(admin.ModelAdmin):
    list_display = ('support_telegram', 'support_phone', 'support_email', 'updated_at')


@admin.register(VideoInstruction)
class VideoInstructionAdmin(admin.ModelAdmin):
    list_display = ('title_uz', 'is_active', 'order')
    list_filter = ('is_active',)


@admin.register(LiveStream)
class LiveStreamAdmin(SimpleHistoryAdmin):
    list_display = ('title_uz', 'status', 'starts_at')
    list_filter = ('status',)
    search_fields = ('title_uz', 'title_ru')


@admin.register(LiveStreamWinner)
class LiveStreamWinnerAdmin(admin.ModelAdmin):
    list_display = ('live_stream', 'user', 'prize_text_uz', 'announced_at')
    autocomplete_fields = ('user',)


@admin.register(MonthlyReminderSettings)
class MonthlyReminderSettingsAdmin(admin.ModelAdmin):
    list_display = ('is_enabled', 'send_day', 'send_hour', 'updated_at')


@admin.register(MonthlyReminderLog)
class MonthlyReminderLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'month', 'sent_at', 'is_successful')
    list_filter = ('is_successful',)
    search_fields = ('user__first_name',)
