"""
Admin configuration for core models.
"""
import zipfile
import os
from django.contrib import admin
from rangefilter.filters import DateTimeRangeFilterBuilder, DateRangeFilterBuilder
class NoDeleteAdminMixin:
    """Отключает удаление везде в админке (включая action «Удалить выбранные»)."""

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from django.utils import timezone
from django.utils.html import format_html
from django.urls import path, reverse
from django.shortcuts import render, redirect
from django.template.response import TemplateResponse
from django.contrib import messages
from django.conf import settings
from django.db import models
from django.db.models import ProtectedError
from simple_history.admin import SimpleHistoryAdmin
from .models import (
    TelegramUser, QRCode, QRCodeScanAttempt, PromoCodeAttempt,
    Gift, GiftRedemption, BroadcastMessage, RegionMessageLog, Promotion, PrivacyPolicy,
    AdminContactSettings, VideoInstruction, MonthlyPromoTicket,
    MonthlyReminderSettings, MonthlyReminderLog,
    LiveStream, LiveStreamWinner,
    UzRegion, UzDistrict,
    Store, QRCodeBatch, SellerPointsTransaction,
    PendingSellerRequest, SellerRegistrationCode,
    ActivityLog,
    Seller, SellerBatch,
)
from .utils import generate_qr_code_image, generate_qr_codes_batch


class StoreAttachedFilter(admin.SimpleListFilter):
    """JIP: Sotuvchining do'koniga biriktirilganlik filtri (avval SmartUP)."""
    title = "Do'kon biriktirilgan"
    parameter_name = 'has_store'

    def lookups(self, request, model_admin):
        return (
            ('yes', "Do'kon biriktirilgan"),
            ('no', "Do'konsiz"),
        )

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(owned_stores__isnull=False).distinct()
        if self.value() == 'no':
            return queryset.filter(user_type='sotuvchi', owned_stores__isnull=True)
        return queryset


class ScannedQRCodeInline(admin.TabularInline):
    """Инлайн: успешно отсканированные промокоды пользователем (readonly)."""
    model = QRCode
    fk_name = 'scanned_by'
    extra = 0
    can_delete = False
    can_add = False
    max_num = 0
    readonly_fields = ['serial_number', 'store', 'batch', 'points', 'scanned_at']
    fields = ['serial_number', 'store', 'batch', 'points', 'scanned_at']
    ordering = ['-scanned_at']
    verbose_name = 'Отсканированный промокод'
    verbose_name_plural = 'Отсканированные промокоды'

    def get_queryset(self, request):
        return super().get_queryset(request).filter(is_scanned=True, is_deleted=False)


class PromoCodeAttemptInline(admin.TabularInline):
    """Инлайн: попытки ввода промокода (успешные и неуспешные)."""
    model = PromoCodeAttempt
    extra = 0
    can_delete = False
    readonly_fields = ['raw_code', 'attempted_at', 'is_successful', 'source']
    fields = ['attempted_at', 'raw_code', 'is_successful', 'source']
    ordering = ['-attempted_at']
    verbose_name = 'Попытка ввода промокода'
    verbose_name_plural = 'Попытки ввода промокодов'


@admin.register(UzRegion)
class UzRegionAdmin(NoDeleteAdminMixin, admin.ModelAdmin):
    """Справочник вилоятов — admin paneldan yashirilgan (user talab).
    Autocomplete uchun ishlatiladi (TelegramUser, Store), shu sababli
    search_fields qoldirildi. Model DB da saqlanadi.
    """

    def has_module_permission(self, request):
        return False

    list_display = ['code', 'name_uz', 'name_ru']
    search_fields = ['code', 'name_uz', 'name_ru']
    ordering = ['code']


@admin.register(UzDistrict)
class UzDistrictAdmin(NoDeleteAdminMixin, admin.ModelAdmin):
    """Справочник туманов — admin paneldan yashirilgan (user talab).
    Autocomplete uchun ishlatiladi (Store.district). Model DB da saqlanadi.
    """

    def has_module_permission(self, request):
        return False

    list_display = ['region', 'code', 'name_uz', 'name_ru']
    list_filter = ['region']
    search_fields = ['code', 'name_uz', 'name_ru', 'region__name_uz', 'region__name_ru']
    autocomplete_fields = ['region']
    list_select_related = ['region']
    ordering = ['region__code', 'code']


@admin.register(TelegramUser)
class TelegramUserAdmin(NoDeleteAdminMixin, SimpleHistoryAdmin):
    """Админка для пользователей Telegram."""
    inlines = [ScannedQRCodeInline, PromoCodeAttemptInline]
    list_display = [
        'user_display', 'phone_number', 'region_display', 'district_display',
        'points_display', 'language_badge',
        'status_badge', 'created_at', 'send_message_button'
    ]
    list_filter = [
        'is_active', 'language', 'region', 'district',
        ('created_at', DateTimeRangeFilterBuilder(title='Дата регистрации (диапазон)')),
    ]
    search_fields = ['telegram_id', 'username', 'first_name', 'phone_number']
    readonly_fields = [
        'telegram_id', 'created_at', 'updated_at',
        'last_message_sent_at', 'blocked_bot_at',
        'points_display', 'total_earned_points', 'open_in_yandex_maps',
        'scan_attempt_count', 'scan_attempt_success_count', 'scan_attempt_unsuccess_count',
    ]
    autocomplete_fields = ['region', 'district']
    ordering = ['region__code', 'district__code', '-created_at']
    actions = [
        'send_personal_message_action', 'update_locations_action',
        'delete_users_action',
    ]
    list_per_page = 50
    date_hierarchy = 'created_at'
    change_list_template = 'admin/core/telegramuser/change_list.html'

    class Media:
        css = {'all': ('core_admin/css/changelist_filters.css',)}
        js = ('core_admin/js/changelist_filters.js',)

    def get_queryset(self, request):
        """Sotuvchi (user_type='sotuvchi') foydalanuvchilarini menyu/ro'yxatdan yashiramiz.

        Yangi tizimda Sotuvchi alohida `Seller` modeli — admin paneldan
        qo'lda boshqariladi. Eski sotuvchi TelegramUser yozuvlari bazada
        qoladi, lekin admin ko'rinishidan chiqariladi.
        """
        qs = super().get_queryset(request)
        return qs.exclude(user_type='sotuvchi')

    def changelist_view(self, request, extra_context=None):
        from django.urls import reverse
        extra_context = extra_context or {}
        if request.user.has_perm('core.send_region_messages'):
            extra_context['send_region_message_url'] = reverse('admin:core_telegramuser_send_region_message')
        return super().changelist_view(request, extra_context)

    def user_display(self, obj):
        """Отображает пользователя с иконкой и ссылкой."""
        icon = "⚡" if obj.user_type == 'santenik' else "🛒"
        name = obj.first_name or "Пользователь"
        username = f"@{obj.username}" if obj.username else ""
        return format_html(
            '<span style="font-size: 18px;">{}</span> <strong>{}</strong> <span style="color: #718096;">{}</span><br>'
            '<span style="color: #718096; font-size: 12px;">ID: {}</span>',
            icon, name, username, obj.telegram_id
        )

    user_display.short_description = 'Пользователь'
    user_display.admin_order_field = 'first_name'

    def points_display(self, obj):
        """Отображает баллы с цветом (вычисляются динамически: промокоды − активные заказы)."""
        if obj is None:
            return '-'
        try:
            calculated = obj.calculate_points()
        except Exception:
            calculated = obj.points
        points_formatted = f"{calculated:,}".replace(",", " ")
        return format_html(
            '<span style="color: #667eea; font-weight: 700; font-size: 16px;">{} баллов</span>',
            points_formatted
        )

    points_display.short_description = 'Баллы (промокоды − заказы)'
    points_display.admin_order_field = 'points'

    def total_earned_points(self, obj):
        """Сумма всех баллов по отсканированным промокодам (без вычета заказов)."""
        if obj is None:
            return 0
        from django.db.models import Sum
        total = QRCode.objects.filter(
            scanned_by=obj,
            is_scanned=True,
            is_deleted=False,
        ).aggregate(total=Sum('points'))['total'] or 0
        return total

    total_earned_points.short_description = 'Points'

    def language_badge(self, obj):
        """Отображает язык с цветным badge."""
        colors = {
            'uz_latin': ('#dbeafe', '#1e40af', '🇺🇿'),
            'ru': ('#fee2e2', '#991b1b', '🇷🇺'),
        }
        bg, text, flag = colors.get(obj.language, ('#f3f4f6', '#374151', '🌐'))
        label = dict(obj._meta.get_field('language').choices).get(obj.language, obj.language)
        return format_html(
            '<span style="background: {}; color: {}; padding: 4px 12px; border-radius: 12px; '
            'font-size: 12px; font-weight: 600;">{} {}</span>',
            bg, text, flag, label.split('(')[0].strip()
        )

    language_badge.short_description = 'Язык'
    language_badge.admin_order_field = 'language'

    def status_badge(self, obj):
        """Отображает статус активности."""
        if obj.is_active:
            return format_html(
                '<span style="background: #d4edda; color: #155724; padding: 4px 12px; border-radius: 12px; '
                'font-size: 12px; font-weight: 600;">✅ Активен</span>'
            )
        else:
            return format_html(
                '<span style="background: #f8d7da; color: #721c24; padding: 4px 12px; border-radius: 12px; '
                'font-size: 12px; font-weight: 600;">❌ Неактивен</span>'
            )

    status_badge.short_description = 'Статус'
    status_badge.admin_order_field = 'is_active'

    def region_display(self, obj):
        """Отображает область пользователя."""
        region_name = obj.get_region_display('ru')
        if region_name:
            return format_html(
                '<span style="background: #e0e7ff; color: #3730a3; padding: 4px 12px; border-radius: 12px; '
                'font-size: 12px; font-weight: 600;">📍 {}</span>',
                region_name
            )
        elif obj.latitude and obj.longitude:
            return format_html(
                '<span style="color: #718096; font-size: 12px;">Не определено</span>'
            )
        else:
            return format_html(
                '<span style="color: #cbd5e0; font-size: 12px;">-</span>'
            )

    region_display.short_description = 'Область'
    region_display.admin_order_field = 'region__code'

    def district_display(self, obj):
        """Отображает район пользователя."""
        district_name = obj.get_district_display('ru')
        if district_name:
            return format_html(
                '<span style="background: #fef3c7; color: #92400e; padding: 4px 12px; border-radius: 12px; '
                'font-size: 12px; font-weight: 600;">🏘️ {}</span>',
                district_name
            )
        elif obj.latitude and obj.longitude:
            return format_html(
                '<span style="color: #718096; font-size: 12px;">Не определено</span>'
            )
        else:
            return format_html(
                '<span style="color: #cbd5e0; font-size: 12px;">-</span>'
            )

    district_display.short_description = 'Район'
    district_display.admin_order_field = 'district__code'

    def open_in_yandex_maps(self, obj):
        """Кнопка для открытия координат пользователя в Яндекс.Картах."""
        if obj is None or obj.latitude is None or obj.longitude is None:
            return format_html('<span style="color: #9ca3af;">Координаты не указаны</span>')
        url = f"https://yandex.ru/maps/?ll={obj.longitude},{obj.latitude}&pt={obj.longitude},{obj.latitude}&z=16"
        return format_html(
            '<a href="{}" target="_blank" rel="noopener noreferrer" '
            'style="display: inline-block; padding: 8px 16px; background: #fc3f1d; color: #fff; '
            'text-decoration: none; border-radius: 6px; font-weight: 500;">'
            'Открыть на Яндекс.Картах</a>',
            url
        )

    open_in_yandex_maps.short_description = 'Яндекс.Карты'

    def scan_attempt_count(self, obj):
        """Общее количество попыток ввода промокода (PromoCodeAttempt)."""
        if obj is None:
            return '-'
        return PromoCodeAttempt.objects.filter(user=obj).count()

    scan_attempt_count.short_description = 'Jami urinishlar soni'

    def scan_attempt_success_count(self, obj):
        """Количество успешных попыток ввода промокода."""
        if obj is None:
            return '-'
        return PromoCodeAttempt.objects.filter(user=obj, is_successful=True).count()

    scan_attempt_success_count.short_description = 'Muvaffaqiyatli urinishlar soni'

    def scan_attempt_unsuccess_count(self, obj):
        """Количество неуспешных попыток ввода промокода."""
        if obj is None:
            return '-'
        return PromoCodeAttempt.objects.filter(user=obj, is_successful=False).count()

    scan_attempt_unsuccess_count.short_description = 'Skaner qilingan promokod urunishlar soni'

    fieldsets = (
        ('Основная информация', {
            'fields': (
                'telegram_id', 'username', 'first_name', 'last_name',
                'scan_attempt_count', 'scan_attempt_success_count', 'scan_attempt_unsuccess_count',
            )
        }),
        ('Контактные данные', {
            'fields': ('phone_number', 'latitude', 'longitude', 'open_in_yandex_maps', 'region', 'district')
        }),
        ('Тип и баллы', {
            'fields': ('user_type', 'points_display', 'total_earned_points'),
        }),
        ('Настройки', {
            'fields': ('language',)
        }),
        ('Активность', {
            'fields': (
                'is_active',
                'last_message_sent_at',
                'blocked_bot_at',
                'promo_failed_attempts',
                'promo_block_stage',
                'promo_blocked_until',
            )
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at')
        }),
    )

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

    def get_readonly_fields(self, request, obj=None):
        """Управляет readonly полями в зависимости от роли пользователя."""
        readonly = list(super().get_readonly_fields(request, obj))

        # Если пользователь имеет пермишн call center и не является superuser
        if not request.user.is_superuser and request.user.has_perm('core.change_user_type_call_center'):
            # Получаем только конкретные поля модели (не обратные связи)
            model_fields = [
                f.name for f in TelegramUser._meta.get_fields()
                if isinstance(f, models.Field) and hasattr(f, 'name')
            ]
            # Исключаем user_type - это единственное поле, которое Call Center может менять
            fields_to_make_readonly = [f for f in model_fields if f != 'user_type']

            # Добавляем все поля в readonly, кроме user_type
            for field in fields_to_make_readonly:
                if field not in readonly:
                    readonly.append(field)
        # Для обычных админов (не superuser и не Call Center) user_type доступен для редактирования
        # Он не в списке readonly_fields, поэтому будет доступен по умолчанию

        return readonly

    def send_personal_message_action(self, request, queryset):
        """Действие для отправки персонального сообщения."""
        from django.shortcuts import render
        from django import forms

        class MessageForm(forms.Form):
            message = forms.CharField(widget=forms.Textarea, label='Текст сообщения')
            parse_mode = forms.ChoiceField(
                choices=[('', 'Без форматирования'), ('HTML', 'HTML'), ('Markdown', 'Markdown')],
                required=False,
                label='Режим парсинга'
            )

        if request.method == 'POST':
            form = MessageForm(request.POST)
            if form.is_valid():
                message_text = form.cleaned_data['message']
                parse_mode = form.cleaned_data['parse_mode'] or None

                import asyncio
                from django.conf import settings
                from aiogram import Bot
                from core.messaging import send_personal_message

                async def send_messages():
                    bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
                    try:
                        sent = 0
                        failed = 0
                        for user in queryset:
                            success, error = await send_personal_message(
                                bot=bot,
                                telegram_id=user.telegram_id,
                                text=message_text,
                                parse_mode=parse_mode
                            )
                            if success:
                                sent += 1
                            else:
                                failed += 1
                        return sent, failed
                    finally:
                        await bot.session.close()

                sent, failed = asyncio.run(send_messages())
                self.message_user(
                    request,
                    f'Отправлено: {sent}, Ошибок: {failed}',
                    level=messages.SUCCESS if failed == 0 else messages.WARNING
                )
                return redirect('admin:core_telegramuser_changelist')
        else:
            form = MessageForm()

        from django.template.response import TemplateResponse

        context = {
            **self.admin_site.each_context(request),
            'form': form,
            'users': queryset,
            'title': 'Отправить сообщение пользователям',
            'opts': self.model._meta,
            'has_view_permission': True,
            'has_add_permission': False,
            'has_change_permission': False,
            'has_delete_permission': False,
        }

        return TemplateResponse(request, 'admin/core/telegramuser/send_message.html', context)

    send_personal_message_action.short_description = 'Отправить персональное сообщение выбранным пользователям'

    def get_search_results(self, request, queryset, search_term):
        """Кастомный поиск с поддержкой поиска по последним 4 цифрам номера телефона."""
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)

        # Если поисковый запрос состоит из 4 цифр, ищем по последним 4 цифрам номера телефона
        if search_term and len(search_term) == 4 and search_term.isdigit():
            from django.db.models import Q, CharField
            from django.db.models.functions import Right, Replace

            # Ищем номера телефонов, которые заканчиваются на эти 4 цифры
            # Учитываем разные форматы номеров (с пробелами, дефисами, плюсами и т.д.)
            # Используем регулярное выражение для поиска номеров, заканчивающихся на эти 4 цифры
            # Паттерн ищет номера, которые заканчиваются на эти 4 цифры (возможно с разделителями)
            phone_pattern = rf'{search_term}$'

            # Прямой поиск по окончанию
            phone_query = Q(phone_number__endswith=search_term)

            # Поиск с учетом разделителей перед последними 4 цифрами
            # Ищем паттерны типа: -4567,  4567, (4567) и т.д.
            # Регулярное выражение ищет номера, которые заканчиваются на эти 4 цифры
            # с возможными разделителями (пробелы, дефисы, скобки и т.д.) перед ними
            phone_query |= Q(phone_number__iregex=rf'[\s\-\(\)\.]*{search_term}$')

            phone_results = self.model.objects.filter(phone_query)

            # Объединяем результаты
            queryset = queryset | phone_results
            use_distinct = True

        return queryset, use_distinct

    def update_locations_action(self, request, queryset):
        """Обновляет вилоят/туман через Nominatim (OSM) для выбранных пользователей с координатами."""
        updated = 0
        for user in queryset:
            if user.latitude is not None and user.longitude is not None:
                user.refresh_location_from_geocoder()
                user.save(update_fields=['region', 'district'])
                updated += 1

        self.message_user(
            request,
            f'Обновлено локаций (Nominatim): {updated} из {queryset.count()}',
            messages.SUCCESS
        )

    update_locations_action.short_description = 'Обновить вилоят/туман через Nominatim (OSM)'

    def delete_users_action(self, request, queryset):
        """Tanlangan foydalanuvchilarni o'chirish (bog'liq yozuvlar tozalanadi)."""
        ids = list(queryset.values_list('id', flat=True))
        # Do'kon egasi → NULL (do'kon o'chirilamaydi, faqat egasiz qoladi)
        Store.objects.filter(owner_id__in=ids).update(owner=None)
        # Tranzaksiyalar va g'olib yozuvlari — user bilan birga o'chiriladi
        SellerPointsTransaction.objects.filter(seller_id__in=ids).delete()
        LiveStreamWinner.objects.filter(user_id__in=ids).delete()
        # Endi xavfsiz o'chirish
        count, _ = TelegramUser.objects.filter(id__in=ids).delete()
        self.message_user(request, f'✅ {count} ta foydalanuvchi o\'chirildi.', messages.SUCCESS)

    delete_users_action.short_description = '🗑️ Tanlangan foydalanuvchilarni o\'chirish'

    def send_message_button(self, obj):
        """Кнопка отправки сообщения в списке."""
        from django.urls import reverse
        url = reverse('admin:core_telegramuser_send_single_message', args=[obj.pk])
        return format_html(
            '<a href="{}" style="background: #667eea; color: white; padding: 6px 12px; '
            'border-radius: 4px; text-decoration: none; white-space: nowrap; font-size: 12px;">💬 Написать</a>',
            url
        )

    send_message_button.short_description = 'Сообщение'

    def get_urls(self):
        """Добавляет кастомные URL."""
        urls = super().get_urls()
        custom_urls = [
            path('<int:user_id>/send_message/', self.admin_site.admin_view(self.send_single_message_view), name='core_telegramuser_send_single_message'),
            path('send_region_message/', self.admin_site.admin_view(self.send_region_message_view), name='core_telegramuser_send_region_message'),
            path(
                'send_region_message/users_autocomplete/',
                self.admin_site.admin_view(self.region_message_user_autocomplete),
                name='core_telegramuser_region_message_user_autocomplete',
            ),
            path(
                'send_region_message/test_send/',
                self.admin_site.admin_view(self.region_message_test_send),
                name='core_telegramuser_region_message_test_send',
            ),
        ]
        return custom_urls + urls

    def send_single_message_view(self, request, user_id):
        """Страница отправки сообщения конкретному пользователю."""
        from django import forms

        user = TelegramUser.objects.get(pk=user_id)

        class MessageForm(forms.Form):
            message = forms.CharField(widget=forms.Textarea, label='Текст сообщения')
            parse_mode = forms.ChoiceField(
                choices=[('', 'Без форматирования'), ('HTML', 'HTML'), ('Markdown', 'Markdown')],
                required=False,
                label='Режим парсинга'
            )

        if request.method == 'POST':
            form = MessageForm(request.POST)
            if form.is_valid():
                message_text = form.cleaned_data['message']
                parse_mode = form.cleaned_data['parse_mode'] or None

                import asyncio
                from core.messaging import send_personal_message

                async def send():
                    from aiogram import Bot
                    bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
                    try:
                        return await send_personal_message(bot=bot, telegram_id=user.telegram_id, text=message_text,
                                                           parse_mode=parse_mode)
                    finally:
                        await bot.session.close()

                success, error = asyncio.run(send())
                if success:
                    self.message_user(request, f'Сообщение отправлено пользователю {user}', messages.SUCCESS)
                else:
                    self.message_user(request, f'Ошибка: {error}', messages.ERROR)
                return redirect('admin:core_telegramuser_changelist')
        else:
            form = MessageForm()

        context = {
            **self.admin_site.each_context(request),
            'form': form,
            'users': TelegramUser.objects.filter(pk=user_id),
            'title': f'Отправить сообщение: {user}',
            'opts': self.model._meta,
            'has_view_permission': True,
            'has_add_permission': False,
            'has_change_permission': False,
            'has_delete_permission': False,
        }
        return TemplateResponse(request, 'admin/core/telegramuser/send_message.html', context)

    def send_region_message_view(self, request):
        """Страница отправки сообщения по области (с фото, форматированием, ссылками)."""
        from django import forms
        from django.core.exceptions import PermissionDenied
        from core.regions import get_all_regions, get_user_region_code

        if not request.user.has_perm('core.send_region_messages'):
            raise PermissionDenied

        region_choices = [
                             ('', '--- Выберите область ---'),
                             ('all', 'Все регионы'),
                         ] + list(get_all_regions('ru'))

        class RegionMessageForm(forms.Form):
            region = forms.ChoiceField(choices=region_choices, required=True, label='Область')
            message = forms.CharField(widget=forms.Textarea(attrs={'rows': 8}), label='Текст сообщения', required=False)
            image = forms.ImageField(required=False, label='Фото (опционально)')
            user_type_filter = forms.ChoiceField(
                choices=[('', 'Все'), ('santenik', 'Сантехники'), ('seller', 'Продавцы')],
                required=False,
                label='Тип пользователя'
            )
            language_filter = forms.ChoiceField(
                choices=[('', 'Все языки'), ('uz_latin', "O'zbek (Lotin)"), ('ru', 'Русский')],
                required=False,
                label='Язык пользователя'
            )
            scheduled_at = forms.DateTimeField(
                required=False,
                label='Отложенная отправка',
                input_formats=['%Y-%m-%dT%H:%M', '%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M'],
                widget=forms.DateTimeInput(
                    attrs={'type': 'datetime-local', 'class': 'vDateField'},
                    format='%Y-%m-%dT%H:%M',
                ),
                help_text='Время в часовом поясе сервера (Asia/Tashkent). Оставьте пустым для немедленной отправки.',
            )

            def clean_scheduled_at(self):
                from django.utils import timezone as _tz
                value = self.cleaned_data.get('scheduled_at')
                if value is None:
                    return None
                # Если форма вернула naive datetime — приводим к таймзоне проекта.
                if _tz.is_naive(value):
                    value = _tz.make_aware(value, _tz.get_current_timezone())
                if value <= _tz.now():
                    raise forms.ValidationError('Время отложенной отправки должно быть в будущем.')
                return value

        if request.method == 'POST':
            form = RegionMessageForm(request.POST, request.FILES)
            if form.is_valid():
                region_code = form.cleaned_data['region']
                message_text = form.cleaned_data.get('message') or ''
                image_file = form.cleaned_data.get('image')
                user_type_filter = form.cleaned_data['user_type_filter'] or None
                language_filter = form.cleaned_data.get('language_filter') or None
                scheduled_at = form.cleaned_data.get('scheduled_at')

                users_qs = TelegramUser.objects.filter(is_active=True)
                if user_type_filter:
                    users_qs = users_qs.filter(user_type=user_type_filter)
                if language_filter:
                    users_qs = users_qs.filter(language=language_filter)

                if region_code == 'all':
                    filtered = list(users_qs)
                else:
                    users = list(users_qs.filter(
                        latitude__isnull=False,
                        longitude__isnull=False,
                    ))
                    filtered = [
                        u for u in users
                        if get_user_region_code(u) == region_code
                    ]

                if not filtered:
                    msg = 'Нет активных пользователей.' if region_code == 'all' else 'В выбранной области нет пользователей с координатами.'
                    self.message_user(request, msg, messages.WARNING)
                else:
                    from core.tasks import send_region_message_task, REGION_MESSAGE_ASYNC_THRESHOLD
                    from core.messaging import TELEGRAM_MESSAGE_DELAY

                    n = len(filtered)

                    # Отложенная рассылка: только пишем в БД со статусом 'pending'.
                    # Celery Beat (см. CELERY_BEAT_SCHEDULE) раз в минуту опрашивает
                    # RegionMessageLog и запускает рассылки, у которых наступило время.
                    # Очередь не зависит от состояния Redis — переживает перезапуск.
                    if scheduled_at:
                        import os as _os
                        import uuid as _uuid
                        from django.core.files.storage import default_storage
                        from django.core.files.base import ContentFile

                        image_storage_path = ''
                        if image_file:
                            ext = _os.path.splitext(image_file.name)[1] or '.jpg'
                            name = f'region_messages/{_uuid.uuid4().hex}{ext}'
                            default_storage.save(name, ContentFile(image_file.read()))
                            image_storage_path = name

                        RegionMessageLog.objects.create(
                            region_code=region_code,
                            user_type_filter=user_type_filter,
                            language_filter=language_filter,
                            total=n,
                            status='pending',
                            initiated_by=request.user,
                            scheduled_at=scheduled_at,
                            message_text=message_text,
                            image_storage_path=image_storage_path,
                        )
                        self.message_user(
                            request,
                            f'Рассылка запланирована на {scheduled_at.strftime("%Y-%m-%d %H:%M")} '
                            f'({n} получателей). Beat-сканер проверяет очередь раз в минуту. '
                            'См. «Логи рассылок по областям».',
                            messages.SUCCESS,
                        )
                        return redirect('admin:core_regionmessagelog_changelist')

                    # Большая рассылка — Celery worker bo'lmasa thread orqali fonda
                    # (Railway'da Celery worker yo'q — sync ham ishlamaydi katta sonlar uchun)
                    if n > REGION_MESSAGE_ASYNC_THRESHOLD:
                        import os
                        import uuid
                        import threading
                        import logging as _bg_logging
                        from django.core.files.storage import default_storage
                        from django.core.files.base import ContentFile

                        _bg_logger = _bg_logging.getLogger(__name__)

                        image_storage_path = ''
                        if image_file:
                            ext = os.path.splitext(image_file.name)[1] or '.jpg'
                            name = f'region_messages/{uuid.uuid4().hex}{ext}'
                            default_storage.save(name, ContentFile(image_file.read()))
                            image_storage_path = name

                        log = RegionMessageLog.objects.create(
                            region_code=region_code,
                            user_type_filter=user_type_filter,
                            language_filter=language_filter,
                            total=n,
                            status='running',
                            initiated_by=request.user,
                            message_text=message_text,
                            image_storage_path=image_storage_path,
                        )

                        celery_ok = False
                        try:
                            send_region_message_task.delay(
                                log_id=log.id,
                                region_code=region_code,
                                message_text=message_text,
                                image_storage_path=image_storage_path,
                                user_type_filter=user_type_filter,
                                language_filter=language_filter,
                            )
                            celery_ok = True
                            self.message_user(
                                request,
                                f'Рассылка по области запущена в фоне через Celery '
                                f'({n} пользователей). Результаты — в разделе '
                                f'«Логи рассылок по областям».',
                                messages.SUCCESS,
                            )
                        except Exception as celery_exc:
                            _bg_logger.warning(
                                "Celery .delay failed (%s) — fallback to thread", celery_exc,
                            )
                            # Thread orqali fon rejimida bajaramiz
                            def _bg_send(log_id, region_code, message_text, image_path, utf, lf):
                                try:
                                    from core.tasks import send_region_message_task as _task
                                    # Celery shared_task.run() — bevosita chaqirish
                                    _task.run(
                                        log_id=log_id,
                                        region_code=region_code,
                                        message_text=message_text,
                                        image_storage_path=image_path,
                                        user_type_filter=utf,
                                        language_filter=lf,
                                    )
                                except Exception as e:
                                    _bg_logger.exception("background region send failed: %s", e)
                                    from django.utils import timezone as _tz_bg
                                    try:
                                        RegionMessageLog.objects.filter(pk=log_id).update(
                                            status='failed',
                                            error_message=f'BG thread xato: {e}',
                                            completed_at=_tz_bg.now(),
                                        )
                                    except Exception:
                                        pass

                            t = threading.Thread(
                                target=_bg_send,
                                args=(log.id, region_code, message_text, image_storage_path,
                                      user_type_filter, language_filter),
                                daemon=True,
                            )
                            t.start()
                            self.message_user(
                                request,
                                f'⚠️ Celery worker yo\'q ({celery_exc.__class__.__name__}) — '
                                f'thread orqali fonda yuborilmoqda ({n} foydalanuvchi). '
                                f'Tarixda holatni kuzating.',
                                messages.WARNING,
                            )
                        return redirect('admin:core_regionmessagelog_changelist')

                    # Небольшая рассылка — сразу в этом запросе
                    import asyncio
                    import tempfile
                    import os
                    import traceback
                    import logging as _logging
                    _logger = _logging.getLogger(__name__)

                    photo_path = None
                    if image_file:
                        ext = os.path.splitext(image_file.name)[1] or '.jpg'
                        with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
                            for chunk in image_file.chunks():
                                tmp.write(chunk)
                            photo_path = tmp.name

                    async def send_all():
                        from aiogram import Bot
                        bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
                        sent, failed = 0, 0
                        try:
                            for i, user in enumerate(filtered):
                                from core.messaging import send_message_to_user
                                success, err = await send_message_to_user(
                                    bot=bot, user=user, text=message_text,
                                    parse_mode='HTML', photo_path=photo_path,
                                    disable_link_preview=True,
                                )
                                if success:
                                    sent += 1
                                else:
                                    failed += 1
                                if i < len(filtered) - 1:
                                    await asyncio.sleep(TELEGRAM_MESSAGE_DELAY)
                            return sent, failed
                        finally:
                            await bot.session.close()
                            if photo_path and os.path.exists(photo_path):
                                try:
                                    os.unlink(photo_path)
                                except OSError:
                                    pass

                    try:
                        # asgiref async_to_sync — Django ichida ishlatish uchun xavfsiz
                        from asgiref.sync import async_to_sync
                        sent, failed = async_to_sync(send_all)()
                    except Exception as send_exc:
                        tb = traceback.format_exc()
                        _logger.exception("region_message send_all failed: %s", send_exc)
                        from django.utils import timezone as _tz
                        RegionMessageLog.objects.create(
                            region_code=region_code,
                            user_type_filter=user_type_filter,
                            language_filter=language_filter,
                            total=len(filtered),
                            sent_count=0,
                            failed_count=len(filtered),
                            status='failed',
                            initiated_by=request.user,
                            message_text=message_text,
                            error_message=f"{send_exc}\n\n{tb}"[:5000],
                            completed_at=_tz.now(),
                        )
                        self.message_user(
                            request,
                            f'❌ Yuborishda xato: {send_exc}. Tarixda batafsil.',
                            messages.ERROR,
                        )
                        return redirect('admin:core_regionmessagelog_changelist')

                    # RegionMessageLog yozuv (kichik rassılka uchun ham)
                    from django.utils import timezone as _tz
                    RegionMessageLog.objects.create(
                        region_code=region_code,
                        user_type_filter=user_type_filter,
                        language_filter=language_filter,
                        total=len(filtered),
                        sent_count=sent,
                        failed_count=failed,
                        status='completed',
                        initiated_by=request.user,
                        message_text=message_text,
                        completed_at=_tz.now(),
                    )

                    self.message_user(
                        request,
                        f'✅ Yuborildi: {sent}, xatolar: {failed} (jami {len(filtered)} ta foydalanuvchi). '
                        f'Tarixni quyidagi sahifada ko\'rishingiz mumkin.',
                        messages.SUCCESS
                    )
                    return redirect('admin:core_regionmessagelog_changelist')
        else:
            form = RegionMessageForm()

        context = {
            **self.admin_site.each_context(request),
            'form': form,
            'title': 'Отправить сообщение по области',
            'opts': self.model._meta,
            'region_message_user_autocomplete_url': reverse(
                'admin:core_telegramuser_region_message_user_autocomplete'
            ),
            'region_message_test_send_url': reverse(
                'admin:core_telegramuser_region_message_test_send'
            ),
        }
        return TemplateResponse(request, 'admin/core/telegramuser/send_region_message.html', context)

    def _telegram_user_autocomplete_label(self, user):
        name = ' '.join(x for x in [user.first_name, user.last_name] if x) or '—'
        un = f' @{user.username}' if user.username else ''
        return f'#{user.id} · tg {user.telegram_id} · {name}{un}'

    def region_message_user_autocomplete(self, request):
        from django.core.exceptions import PermissionDenied

        if not request.user.has_perm('core.send_region_messages'):
            raise PermissionDenied
        term = (request.GET.get('q') or request.GET.get('term') or '').strip()
        try:
            page = max(1, int(request.GET.get('page', 1)))
        except ValueError:
            page = 1
        page_size = 20
        start = (page - 1) * page_size
        end = start + page_size + 1

        qs = TelegramUser.objects.all().order_by('-id')
        if term:
            q = (
                Q(username__icontains=term)
                | Q(first_name__icontains=term)
                | Q(last_name__icontains=term)
                | Q(phone_number__icontains=term)
            )
            if term.isdigit():
                try:
                    n = int(term)
                    q |= Q(telegram_id=n) | Q(pk=n)
                except OverflowError:
                    pass
            qs = qs.filter(q)

        batch = list(qs[start:end])
        has_more = len(batch) > page_size
        batch = batch[:page_size]
        results = [
            {'id': str(u.id), 'text': self._telegram_user_autocomplete_label(u)}
            for u in batch
        ]
        return JsonResponse({'results': results, 'pagination': {'more': has_more}})

    def region_message_test_send(self, request):
        """Тестовая отправка: тот же текст/фото, что в форме рассылки по области."""
        from django.core.exceptions import PermissionDenied
        import asyncio
        import tempfile

        if request.method != 'POST':
            return JsonResponse({'ok': False, 'error': 'Только POST'}, status=405)
        if not request.user.has_perm('core.send_region_messages'):
            raise PermissionDenied

        raw_uid = request.POST.get('test_user_id')
        message_text = request.POST.get('message', '')
        image_file = request.FILES.get('image')

        try:
            uid = int(raw_uid)
        except (TypeError, ValueError):
            return JsonResponse({'ok': False, 'error': 'Выберите пользователя'}, status=400)

        try:
            user = TelegramUser.objects.get(pk=uid)
        except TelegramUser.DoesNotExist:
            return JsonResponse({'ok': False, 'error': 'Пользователь не найден'}, status=404)

        photo_path = None
        if image_file:
            ext = os.path.splitext(image_file.name)[1] or '.jpg'
            tmp = tempfile.NamedTemporaryFile(delete=False, suffix=ext)
            try:
                for chunk in image_file.chunks():
                    tmp.write(chunk)
                tmp.close()
                photo_path = tmp.name
            except Exception:
                tmp.close()
                if os.path.exists(tmp.name):
                    try:
                        os.unlink(tmp.name)
                    except OSError:
                        pass
                return JsonResponse({'ok': False, 'error': 'Не удалось сохранить изображение'}, status=400)

        async def _send():
            from aiogram import Bot
            from core.messaging import send_message_to_user

            bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
            try:
                return await send_message_to_user(
                    bot=bot,
                    user=user,
                    text=message_text,
                    parse_mode='HTML',
                    photo_path=photo_path,
                    disable_link_preview=True,
                )
            finally:
                await bot.session.close()

        try:
            ok, err = asyncio.run(_send())
        except Exception as exc:
            ok, err = False, str(exc)
        finally:
            if photo_path and os.path.exists(photo_path):
                try:
                    os.unlink(photo_path)
                except OSError:
                    pass

        if ok:
            return JsonResponse({'ok': True, 'detail': f'Сообщение отправлено: {user}'})
        return JsonResponse({'ok': False, 'error': err or 'Не удалось отправить'}, status=400)


class QRCodeScanAttemptInline(admin.TabularInline):
    """Инлайн для попыток сканирования."""
    model = QRCodeScanAttempt
    extra = 0
    readonly_fields = ['user', 'attempted_at', 'is_successful']
    can_delete = False


@admin.register(QRCode)
class QRCodeAdmin(NoDeleteAdminMixin, SimpleHistoryAdmin):
    """Админка для QR-кодов (только просмотр)."""
    change_form_template = 'admin/core/qrcode/change_form.html'
    changelist_template = 'admin/core/qrcode/change_list.html'
    list_display = [
        'qr_display', 'store_badge', 'batch_display', 'points_display',
        'status_badge', 'scanned_by_display', 'generated_at'
    ]
    list_filter = [
        'store', 'batch', 'is_scanned', 'is_deleted',
    ]
    search_fields = ['code', 'hash_code', 'serial_number', 'store__name', 'batch__name']
    readonly_fields = [
        'code', 'hash_code', 'serial_number', 'store', 'batch',
        'points', 'generated_at', 'scanned_at', 'scanned_by', 'is_scanned', 'is_deleted',
    ]
    ordering = ['-generated_at']
    inlines = [QRCodeScanAttemptInline]
    list_per_page = 50
    date_hierarchy = 'generated_at'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Только changelist: иначе нельзя открыть карточку удалённого QR по прямой ссылке
        if (
                request.resolver_match
                and request.resolver_match.url_name.endswith('_changelist')
                and 'is_deleted__exact' not in request.GET
        ):
            qs = qs.filter(is_deleted=False)
        return qs

    def has_view_permission(self, request, obj=None):
        """Проверяет права доступа к просмотру QR-кода."""
        # Superuser всегда имеет доступ
        if request.user.is_superuser:
            return True

        # Проверяем custom permission
        if request.user.has_perm('core.view_qrcode_detail'):
            return True

        return False

    def get_list_display_links(self, request, list_display):
        """Скрывает ссылки на детальный просмотр для пользователей без permission."""
        if not self.has_view_permission(request):
            # Если нет доступа к просмотру, не показываем ссылки
            return (None,)
        # По умолчанию Django использует первый элемент list_display как ссылку
        return super().get_list_display_links(request, list_display)

    def get_fields(self, request, obj=None):
        """Возвращает список полей для отображения, скрывая code и hash_code для неиспользованных QR-кодов."""
        fields = list(super().get_fields(request, obj))

        # Всегда скрываем image_path
        if 'image_path' in fields:
            fields.remove('image_path')

        # Скрываем code и hash_code для неиспользованных QR-кодов (безопасность)
        if obj and not obj.is_scanned:
            if 'code' in fields:
                fields.remove('code')
            if 'hash_code' in fields:
                fields.remove('hash_code')
            # Добавляем информационное поле вместо code
            if 'security_notice' not in fields:
                # JIP: code_type olib tashlandi — store yoki batch dan keyin qo'shamiz
                anchor = None
                for candidate in ('batch', 'store'):
                    if candidate in fields:
                        anchor = candidate
                        break
                if anchor is not None:
                    fields.insert(fields.index(anchor) + 1, 'security_notice')
                else:
                    fields.insert(0, 'security_notice')

        # Если пользователь не имеет прав на просмотр деталей, заменяем code на masked_code_display
        elif obj and not self.has_view_permission(request, obj):
            # Сохраняем индекс code перед удалением
            code_index = None
            if 'code' in fields:
                code_index = fields.index('code')
                fields.remove('code')
            if 'hash_code' in fields:
                fields.remove('hash_code')
            if 'masked_code_display' not in fields:
                # Вставляем masked_code_display на место code
                if code_index is not None:
                    fields.insert(code_index, 'masked_code_display')
                else:
                    # Если code не найден, просто добавляем в начало
                    fields.insert(0, 'masked_code_display')

        return fields

    def get_readonly_fields(self, request, obj=None):
        """Возвращает список readonly полей, добавляя информационное поле для неиспользованных QR-кодов."""
        readonly = list(super().get_readonly_fields(request, obj))

        # Для неиспользованных QR-кодов добавляем информационное поле
        if obj and not obj.is_scanned:
            # Убираем code и hash_code из readonly, так как мы их скрываем
            if 'code' in readonly:
                readonly.remove('code')
            if 'hash_code' in readonly:
                readonly.remove('hash_code')
            # Добавляем security_notice
            if 'security_notice' not in readonly:
                readonly.append('security_notice')

        # Если пользователь не имеет прав на просмотр деталей, маскируем код
        elif obj and not self.has_view_permission(request, obj):
            # Убираем code из readonly, так как мы заменим его на masked_code
            if 'code' in readonly:
                readonly.remove('code')
            if 'hash_code' in readonly:
                readonly.remove('hash_code')
            # Добавляем masked_code вместо code
            if 'masked_code_display' not in readonly:
                readonly.append('masked_code_display')

        return readonly

    def masked_code_display(self, obj):
        """Отображает замаскированный код для пользователей без прав."""
        if obj:
            masked = self.masked_code(obj)
            return format_html(
                '<div style="font-family: monospace; font-size: 14px; color: #333;">'
                '<strong>{}</strong></div>',
                masked
            )
        return '-'

    masked_code_display.short_description = 'Code'

    def security_notice(self, obj):
        """Информационное сообщение о безопасности для неиспользованных QR-кодов."""
        if obj and not obj.is_scanned:
            return format_html(
                '<div style="background: #fff3cd; border: 1px solid #ffc107; border-radius: 8px; '
                'padding: 15px; margin: 10px 0;">'
                '<div style="display: flex; align-items: center; gap: 10px; margin-bottom: 10px;">'
                '<span style="font-size: 20px;">🔒</span>'
                '<strong style="color: #856404; font-size: 14px;">Информация о безопасности</strong>'
                '</div>'
                '<p style="margin: 0; color: #856404; font-size: 13px; line-height: 1.5;">'
                'Код QR-кода скрыт для безопасности, так как QR-код еще не использован. '
                'После сканирования QR-кода пользователем код будет доступен для просмотра.'
                '</p>'
                '<p style="margin: 10px 0 0 0; color: #856404; font-size: 12px;">'
                '<strong>Серийный номер:</strong> {}</p>'
                '</div>',
                obj.serial_number if obj else '-'
            )
        return '-'

    security_notice.short_description = 'Информация'

    def change_view(self, request, object_id, form_url='', extra_context=None):
        """Переопределяем детальный просмотр для проверки прав доступа и маскирования кода."""
        from django.template.response import TemplateResponse

        obj = self.get_object(request, object_id)

        extra_context = extra_context or {}
        # Кнопка «Отменить сканирования» только для superuser
        if request.user.is_superuser:
            from django.urls import reverse
            extra_context['show_clear_scans_button'] = True
            extra_context['clear_scans_url'] = reverse('admin:core_qrcode_clear_scans', args=[object_id])
        else:
            extra_context['show_clear_scans_button'] = False

        # Проверяем права доступа
        if not self.has_view_permission(request, obj):
            # Если нет доступа, показываем кастомный шаблон с сообщением
            extra_context['no_access'] = True
            extra_context['is_superuser'] = request.user.is_superuser
            extra_context['has_permission'] = request.user.has_perm('core.view_qrcode_detail')
            extra_context['title'] = 'Доступ запрещен'
            extra_context['opts'] = self.model._meta
            extra_context['has_view_permission'] = False
            extra_context['has_add_permission'] = False
            extra_context['has_change_permission'] = False
            extra_context['has_delete_permission'] = False

            return TemplateResponse(
                request,
                'admin/core/qrcode/no_access.html',
                extra_context,
                status=403
            )

        return super().change_view(request, object_id, form_url, extra_context)

    def qr_display(self, obj):
        """Отображает QR-код с серийным номером."""
        return format_html(
            '<div style="line-height: 1.6;">'
            '<strong style="font-size: 16px;">📱 #{}</strong><br>'
            '<span style="color: #718096; font-size: 12px; font-family: monospace;">{}</span>',
            obj.serial_number,
            self.masked_code(obj)
        )

    qr_display.short_description = 'QR-код'
    qr_display.admin_order_field = 'serial_number'

    def store_badge(self, obj):
        """JIP: Do'kon nomi badge."""
        if obj.store_id:
            return format_html(
                '<span style="background: #dbeafe; color: #1e40af; padding: 4px 12px; border-radius: 12px; '
                'font-size: 12px; font-weight: 600;">🏪 {}</span>',
                obj.store.name,
            )
        return format_html('<span style="color: #999;">—</span>')

    store_badge.short_description = "Do'kon"
    store_badge.admin_order_field = 'store__name'

    def batch_display(self, obj):
        """JIP: Partiya nomi."""
        if obj.batch_id:
            return format_html('<small>{}</small>', obj.batch.name)
        return '—'

    batch_display.short_description = 'Partiya'
    batch_display.admin_order_field = 'batch__name'

    def points_display(self, obj):
        """Отображает баллы."""
        points_formatted = f"{obj.points:,}"
        return format_html(
            '<span style="color: #667eea; font-weight: 700; font-size: 16px;">{}</span>',
            points_formatted
        )

    points_display.short_description = 'Баллы'
    points_display.admin_order_field = 'points'

    def status_badge(self, obj):
        """Отображает статус сканирования."""
        if obj.is_scanned:
            return format_html(
                '<span style="background: #d4edda; color: #155724; padding: 4px 12px; border-radius: 12px; '
                'font-size: 12px; font-weight: 600;">✅ Использован</span>'
            )
        else:
            return format_html(
                '<span style="background: #fff3cd; color: #856404; padding: 4px 12px; border-radius: 12px; '
                'font-size: 12px; font-weight: 600;">⏳ Не использован</span>'
            )

    status_badge.short_description = 'Статус'
    status_badge.admin_order_field = 'is_scanned'

    def changelist_view(self, request, extra_context=None):
        """Добавляет кнопку для генерации QR-кодов и информацию о доступе."""
        from django.utils import timezone as dj_tz
        extra_context = extra_context or {}
        extra_context['show_generate_button'] = True
        extra_context['has_view_permission'] = self.has_view_permission(request)
        extra_context['show_export_scanned_history'] = (
            self.has_view_permission(request)
            and request.GET.get('is_scanned__exact') == '1'
        )
        extra_context['show_export_monthly'] = self.has_view_permission(request)
        now = dj_tz.now()
        extra_context['export_default_year'] = now.year
        extra_context['export_default_month'] = now.month
        return super().changelist_view(request, extra_context=extra_context)

    def has_add_permission(self, request):
        """Отключаем добавление через админку."""
        return False

    def has_change_permission(self, request, obj=None):
        """Отключаем редактирование."""
        return False

    def masked_code(self, obj):
        """Маскирует часть кода для отображения."""
        if len(obj.code) > 5:
            # Для коротких кодов: E-ABC123 -> E-AB***3
            prefix = obj.code[:3]  # E- или D- + первый символ
            suffix = obj.code[-1]  # Последний символ
            masked = '*' * max(1, len(obj.code) - 4)
            return f"{prefix}{masked}{suffix}"
        return obj.code

    masked_code.short_description = 'Штрих-код'

    def scanned_by_display(self, obj):
        """Отображает пользователя, который отсканировал."""
        if obj.scanned_by:
            return f"{obj.scanned_by.first_name} (@{obj.scanned_by.username or 'N/A'})"
        return '-'

    scanned_by_display.short_description = 'Пользователь Telegram'
    scanned_by_display.admin_order_field = 'scanned_by__first_name'

    def get_urls(self):
        """Добавляет кастомные URL для генерации QR-кодов и отмены сканирований."""
        urls = super().get_urls()
        custom_urls = [
            path('generate/', self.admin_site.admin_view(self.generate_qr_codes_view), name='core_qrcode_generate'),
            path(
                'export_history_xlsx/',
                self.admin_site.admin_view(self.export_history_xlsx_view),
                name='core_qrcode_export_history_xlsx',
            ),
            path(
                'export_monthly_xlsx/',
                self.admin_site.admin_view(self.export_monthly_xlsx_view),
                name='core_qrcode_export_monthly_xlsx',
            ),
            path('<path:object_id>/clear_scans/', self.admin_site.admin_view(self.clear_scans_view), name='core_qrcode_clear_scans'),
        ]
        return custom_urls + urls

    def export_history_xlsx_view(self, request):
        """Экспорт текущего списка промокодов (те же фильтры, что в changelist) в Excel."""
        from django.core.exceptions import PermissionDenied
        from django.contrib.admin.options import IncorrectLookupParameters
        from django.utils import timezone as dj_tz
        from openpyxl import Workbook
        from openpyxl.styles import Font, Alignment
        from openpyxl.utils import get_column_letter

        if not self.has_view_permission(request):
            raise PermissionDenied

        try:
            cl = self.get_changelist_instance(request)
        except IncorrectLookupParameters:
            self.message_user(request, 'Некорректные параметры фильтра.', messages.ERROR)
            return redirect('admin:core_qrcode_changelist')

        qs = cl.queryset.select_related('scanned_by__region', 'scanned_by__district')

        wb = Workbook()
        ws = wb.active
        ws.title = 'Promo'

        headers = [
            'ID промокода',
            'Серийный номер',
            'Тип',
            'Промокод',
            'Хеш',
            'Баллы',
            'Дата генерации',
            'Дата сканирования',
            'user_id',
            'telegram_id',
            'username',
            'Имя',
            'Фамилия',
            'Телефон',
            'Тип пользователя',
            'Регион',
            'Район',
        ]
        ws.append(headers)
        header_font = Font(bold=True)
        for cell in ws[1]:
            cell.font = header_font
            cell.alignment = Alignment(horizontal='center', vertical='center')

        local_tz = dj_tz.get_current_timezone()

        def fmt_local(dt):
            if not dt:
                return ''
            return dt.astimezone(local_tz).strftime('%d.%m.%Y %H:%M:%S')

        for qr in qs.iterator(chunk_size=500):
            user = qr.scanned_by
            ws.append(
                [
                    qr.pk,
                    qr.serial_number,
                    (qr.store.name if qr.store_id else ''),
                    qr.code,
                    qr.hash_code,
                    qr.points,
                    fmt_local(qr.generated_at),
                    fmt_local(qr.scanned_at),
                    user.pk if user else '',
                    user.telegram_id if user else '',
                    (user.username or '') if user else '',
                    (user.first_name or '') if user else '',
                    (user.last_name or '') if user else '',
                    (user.phone_number or '') if user else '',
                    user.get_user_type_display() if user and user.user_type else '',
                    user.region.code if user and user.region_id else '',
                    user.district.code if user and user.district_id else '',
                ]
            )

        widths = [14, 16, 14, 18, 12, 10, 20, 20, 10, 14, 18, 16, 16, 16, 16, 16, 12, 12]
        for idx, width in enumerate(widths, 1):
            ws.column_dimensions[get_column_letter(idx)].width = width

        filename = f'qrcode_list_{dj_tz.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        wb.save(response)
        return response

    def export_monthly_xlsx_view(self, request):
        """Экспорт промокодов за выбранный месяц: два листа — сантехники и продавцы."""
        from django.core.exceptions import PermissionDenied
        from django.utils import timezone as dj_tz
        from openpyxl import Workbook
        from openpyxl.styles import Font, Alignment, PatternFill
        from openpyxl.utils import get_column_letter

        if not self.has_view_permission(request):
            raise PermissionDenied

        now = dj_tz.now()
        try:
            year = int(request.GET.get('year', now.year))
            month = int(request.GET.get('month', now.month))
            if not (1 <= month <= 12) or year < 2020:
                raise ValueError
        except (ValueError, TypeError):
            self.message_user(request, 'Некорректный год или месяц.', messages.ERROR)
            return redirect('admin:core_qrcode_changelist')

        import calendar
        from datetime import datetime, timezone as dt_tz
        month_start = datetime(year, month, 1, tzinfo=dt_tz.utc)
        last_day = calendar.monthrange(year, month)[1]
        month_end = datetime(year, month, last_day, 23, 59, 59, tzinfo=dt_tz.utc)

        month_name = {
            1: 'Январь', 2: 'Февраль', 3: 'Март', 4: 'Апрель',
            5: 'Май', 6: 'Июнь', 7: 'Июль', 8: 'Август',
            9: 'Сентябрь', 10: 'Октябрь', 11: 'Ноябрь', 12: 'Декабрь',
        }[month]

        base_qs = (
            QRCode.objects
            .filter(is_scanned=True, is_deleted=False, scanned_at__gte=month_start, scanned_at__lte=month_end)
            .select_related('scanned_by__region', 'scanned_by__district', 'monthly_ticket')
            .order_by('scanned_at')
        )

        headers = [
            'ID', 'Серийный номер', 'Тип', 'Промокод', 'Баллы',
            'Дата сканирования', '№ в месяце', 'Имя', 'Фамилия', 'Телефон',
            'Telegram ID', 'Username', 'Регион', 'Район',
        ]

        local_tz = dj_tz.get_current_timezone()

        def fmt_local(dt):
            return dt.astimezone(local_tz).strftime('%d.%m.%Y %H:%M:%S') if dt else ''

        def fill_sheet(ws, qs, header_color):
            ws.append(headers)
            fill = PatternFill(start_color=header_color, end_color=header_color, fill_type='solid')
            bold = Font(bold=True)
            for cell in ws[1]:
                cell.font = bold
                cell.alignment = Alignment(horizontal='center', vertical='center')
                cell.fill = fill
            for qr in qs.iterator(chunk_size=500):
                u = qr.scanned_by
                ticket = getattr(qr, 'monthly_ticket', None)
                ws.append([
                    qr.pk,
                    qr.serial_number or '',
                    (qr.store.name if qr.store_id else ''),
                    qr.code,
                    qr.points,
                    fmt_local(qr.scanned_at),
                    ticket.order if ticket else '',
                    (u.first_name or '') if u else '',
                    (u.last_name or '') if u else '',
                    (u.phone_number or '') if u else '',
                    u.telegram_id if u else '',
                    (u.username or '') if u else '',
                    (u.region.code if u and u.region_id else ''),
                    (u.district.code if u and u.district_id else ''),
                ])
            col_widths = [10, 18, 14, 18, 8, 22, 10, 16, 16, 16, 14, 18, 10, 10]
            for idx, w in enumerate(col_widths, 1):
                ws.column_dimensions[get_column_letter(idx)].width = w

        user_type = request.GET.get('user_type', 'all').strip().lower()
        if user_type not in ('santenik', 'seller'):
            user_type = 'all'

        wb = Workbook()
        if user_type == 'all':
            ws_elec = wb.active
            ws_elec.title = 'Сантехники'
            fill_sheet(ws_elec, base_qs.filter(scanned_by__user_type='santenik'), 'D6E4F0')
            ws_sell = wb.create_sheet(title='Продавцы')
            fill_sheet(ws_sell, base_qs.filter(scanned_by__user_type='sotuvchi'), 'D6F0D6')
        elif user_type == 'santenik':
            ws = wb.active
            ws.title = 'Сантехники'
            fill_sheet(ws, base_qs.filter(scanned_by__user_type='santenik'), 'D6E4F0')
        else:
            ws = wb.active
            ws.title = 'Продавцы'
            fill_sheet(ws, base_qs.filter(scanned_by__user_type='sotuvchi'), 'D6F0D6')

        type_suffix = {'santenik': '_santenikar', 'seller': '_sotuvchilar'}.get(user_type, '')
        filename = f'promokody_{month_name}_{year}{type_suffix}.xlsx'
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        wb.save(response)
        return response

    def clear_scans_view(self, request, object_id):
        """Отмена попыток сканирования и сканировавшего пользователя (только для superuser)."""
        from django.core.exceptions import PermissionDenied
        from django.db import transaction

        if not request.user.is_superuser:
            raise PermissionDenied("Только суперадмин может отменять сканирования.")

        obj = self.get_object(request, object_id)
        if obj is None:
            from django.http import Http404
            raise Http404

        if request.method == 'POST':
            with transaction.atomic():
                # Собираем данные до удаления для записи в историю
                previous_scanned_by = obj.scanned_by
                previous_scanned_at = obj.scanned_at
                attempts_before = list(
                    QRCodeScanAttempt.objects.filter(qr_code=obj).select_related('user').order_by('attempted_at')
                )
                deleted_count, _ = QRCodeScanAttempt.objects.filter(qr_code=obj).delete()

                # Формируем подробное описание для истории изменений (до save), читабельно
                lines = ["Отменены сканирования (очистка попыток и сканировавшего пользователя).", ""]
                if previous_scanned_by:
                    lines.append("Сканировавший пользователь (до отмены):")
                    lines.append(
                        f"  id={previous_scanned_by.id}, telegram_id={previous_scanned_by.telegram_id}, "
                        f"{previous_scanned_by.first_name or '-'} (@{previous_scanned_by.username or 'нет'})"
                    )
                    if previous_scanned_at:
                        lines.append(f"  Дата сканирования: {previous_scanned_at.strftime('%Y-%m-%d %H:%M:%S')}")
                    lines.append("")
                else:
                    lines.append("Сканировавшего пользователя не было (QR-код не был использован).")
                    lines.append("")
                lines.append(f"Удалено попыток сканирования: {deleted_count}")
                if attempts_before:
                    lines.append("")
                    lines.append("Детали удалённых попыток:")
                    for a in attempts_before:
                        u = a.user
                        success = "успешно" if a.is_successful else "неуспешно"
                        lines.append(
                            f"  • id={u.id}, telegram_id={u.telegram_id}, "
                            f"{u.first_name or '-'} (@{u.username or 'нет'}), "
                            f"{a.attempted_at.strftime('%Y-%m-%d %H:%M:%S')} — {success}"
                        )
                change_message = "\n".join(lines)

                obj.scanned_by = None
                obj.scanned_at = None
                obj.is_scanned = False
                # Причина для Simple History (страница «История») — полное описание
                obj._change_reason = change_message
                obj.save(update_fields=['scanned_by', 'scanned_at', 'is_scanned'])
                if previous_scanned_by:
                    previous_scanned_by.invalidate_points_cache()
                    # Запись в историю пользователя (TelegramUser): что было отменено, читабельно
                    user_lines = [
                        f"Отменено сканирование по промокоду {obj.serial_number} (QRCode id={obj.id}).",
                        "",
                        "Причина: отмена сканирований в админке (кнопка «Отменить сканирования»).",
                        ""
                    ]
                    if previous_scanned_at:
                        user_lines.append(
                            f"Дата сканирования (до отмены): {previous_scanned_at.strftime('%Y-%m-%d %H:%M:%S')}")
                        user_lines.append("")
                    user_lines.append(f"Удалено попыток по этому QR: {deleted_count}")
                    if attempts_before:
                        user_lines.append("")
                        user_lines.append("Удалённые попытки по этому промокоду:")
                        for a in attempts_before:
                            u = a.user
                            success = "успешно" if a.is_successful else "неуспешно"
                            user_lines.append(
                                f"  • id={u.id}, telegram_id={u.telegram_id}, "
                                f"{u.first_name or '-'} (@{u.username or 'нет'}), "
                                f"{a.attempted_at.strftime('%Y-%m-%d %H:%M:%S')} — {success}"
                            )
                    previous_scanned_by._change_reason = "\n".join(user_lines)
                    previous_scanned_by.save(update_fields=['updated_at'])

                # Полное описание в лог админки (Django LogEntry)
                self.log_change(request, obj, change_message)
            messages.success(
                request,
                f"Сканирования отменены: удалено попыток — {deleted_count}, сброшен сканировавший пользователь."
            )
            return redirect('admin:core_qrcode_change', object_id=object_id)

        # GET — страница подтверждения
        context = {
            **self.admin_site.each_context(request),
            'title': 'Отменить сканирования',
            'object': obj,
            'opts': self.model._meta,
            'object_id': object_id,
            'clear_scans_url': request.path,
        }
        return TemplateResponse(request, 'admin/core/qrcode/clear_scans_confirm.html', context)

    def generate_qr_codes_view(self, request):
        """Promokodlarni ommaviy yaratish (batch'siz).

        Yangi flow:
        - Faqat `quantity` + `points` qabul qiladi
        - Har promokod global `sequence_number` oladi (1..N)
        - Format: `S` + 7 alphanumeric (masalan `S3K9P2L7`)
        - Sotuvchiga keyinchalik `SellerAdmin → Partiyalar` orqali
          range biriktiriladi (promo_from..promo_to)
        """
        if not request.user.is_superuser:
            from django.core.exceptions import PermissionDenied
            raise PermissionDenied("У вас нет прав для генерации QR-кодов.")

        if request.method == 'POST':
            quantity_raw = request.POST.get('quantity', '0')
            points_raw = request.POST.get('points') or '50'

            try:
                quantity = int(quantity_raw)
                points = int(points_raw)
            except (ValueError, TypeError):
                quantity = 0
                points = 50

            if quantity <= 0 or quantity > 30000:
                messages.error(request, "Miqdor 1-30000 oraliqida bo'lishi kerak!")
            elif points <= 0:
                messages.error(request, "Ballar 0 dan katta bo'lishi kerak!")
            else:
                # Railway'da Celery worker yo'q — sinxron yaratamiz.
                import time
                import traceback
                import logging
                from django.utils import timezone as _tz
                from core.models import QRCode, QRCodeBatch

                _logger = logging.getLogger(__name__)
                start = time.time()
                created = 0
                last_err = None
                batch = None

                try:
                    # Generatsiya tarixini yozish uchun batch yaratamiz
                    batch_name = f"PROMO-{_tz.now():%Y%m%d-%H%M%S}-{quantity}"
                    batch = QRCodeBatch.objects.create(
                        name=batch_name,
                        quantity=quantity,
                        points_per_code=points,
                        status='active',
                        created_by=request.user if request.user.is_authenticated else None,
                    )

                    for _ in range(quantity):
                        try:
                            QRCode.create_promo_code(points=points, batch=batch)
                            created += 1
                        except Exception as inner_exc:
                            _logger.exception("create_promo_code failed at #%s", created + 1)
                            last_err = inner_exc
                            break

                    # Batch'ni har qanday holatda yangilash (created=0 bo'lsa ham)
                    batch.completed_at = _tz.now()
                    if created < quantity:
                        # Xato batafsil yozish — created==0 ham
                        tb_str = traceback.format_exc() if last_err else ''
                        batch.error_message = (
                            f"Qisman yaratildi: {created}/{quantity}.\n"
                            f"Xato turi: {type(last_err).__name__ if last_err else 'N/A'}\n"
                            f"Xato: {last_err}\n\n"
                            f"Traceback:\n{tb_str[-2500:]}"
                        )
                        # Agar 0 yaratilgan bo'lsa quantity ni saqlaymiz tushunish uchun
                        if created > 0:
                            batch.quantity = created
                        batch.save(update_fields=['completed_at', 'quantity', 'error_message'])
                    else:
                        batch.save(update_fields=['completed_at'])

                    # xlsx fayl on-demand yaratiladi /admin/qrcodebatch/<id>/xlsx/
                    # (productionda media filelar serve qilinmaydi)

                except Exception as outer_exc:
                    last_err = outer_exc
                    _logger.exception("generate_qr_codes_view fatal")
                    if batch:
                        try:
                            batch.error_message = f"FATAL: {outer_exc}\n{traceback.format_exc()[-2500:]}"
                            batch.save(update_fields=['error_message'])
                        except Exception:
                            pass

                elapsed = time.time() - start
                if created == quantity:
                    messages.success(
                        request,
                        f"✅ {created} ta promokod yaratildi "
                        f"(har biri {points} ball, {elapsed:.1f}s). "
                        f"Tarix: Promokod yaratish tarixi → #{batch.id if batch else '—'}"
                    )
                elif created > 0:
                    messages.warning(
                        request,
                        f"⚠️ {created}/{quantity} ta yaratildi, xato: {last_err}"
                    )
                else:
                    tb = traceback.format_exc() if last_err else ''
                    messages.error(
                        request,
                        f"❌ Promokod yaratilmadi: {last_err}. {tb[-800:]}"
                    )
                return redirect('admin:core_qrcodebatch_changelist')

        context = {
            **self.admin_site.each_context(request),
            'title': 'Promokodlar generatsiyasi',
            'has_permission': request.user.is_superuser,
        }
        return TemplateResponse(request, 'admin/core/qrcode/generate.html', context)


@admin.register(Gift)
class GiftAdmin(NoDeleteAdminMixin, SimpleHistoryAdmin):
    """Админка для подарков (JIP: faqat santenik uchun)."""
    list_display = ['gift_display', 'points_cost_display', 'order', 'image_preview', 'status_badge',
                    'created_at']
    list_filter = [
        'is_active',
        ('created_at', DateTimeRangeFilterBuilder(title='Дата создания (диапазон)')),
    ]
    search_fields = ['name_uz_latin', 'name_ru', 'description_uz_latin', 'description_ru']
    readonly_fields = ['created_at', 'updated_at', 'image_preview']
    list_editable = ['order']
    list_per_page = 25

    def gift_display(self, obj):
        """Отображает подарок с иконкой."""
        name = obj.name_uz_latin or obj.name_ru or 'Без названия'
        return format_html(
            '<span style="font-size: 20px;">🎁</span> <strong style="font-size: 16px;">{}</strong>',
            name
        )

    gift_display.short_description = 'Подарок'
    gift_display.admin_order_field = 'name_uz_latin'

    def points_cost_display(self, obj):
        """Отображает стоимость с цветом."""
        points_formatted = f"{obj.points_cost:,}".replace(",", " ")
        return format_html(
            '<span style="color: #667eea; font-weight: 700; font-size: 16px;">{}</span> баллов',
            points_formatted
        )

    points_cost_display.short_description = 'Стоимость'
    points_cost_display.admin_order_field = 'points_cost'

    def status_badge(self, obj):
        """Отображает статус активности."""
        if obj.is_active:
            return format_html(
                '<span style="background: #d4edda; color: #155724; padding: 4px 12px; border-radius: 12px; '
                'font-size: 12px; font-weight: 600;">✅ Активен</span>'
            )
        else:
            return format_html(
                '<span style="background: #f8d7da; color: #721c24; padding: 4px 12px; border-radius: 12px; '
                'font-size: 12px; font-weight: 600;">❌ Неактивен</span>'
            )

    status_badge.short_description = 'Статус'
    status_badge.admin_order_field = 'is_active'

    def image_preview(self, obj):
        """Превью изображения подарка."""
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 100px; max-width: 100px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);" />',
                obj.image.url
            )
        return '-'

    image_preview.short_description = 'Превью'

    fieldsets = (
        ('Основная информация', {
            'fields': ('name_uz_latin', 'name_ru', 'image', 'image_preview')
        }),
        ('Описание', {
            'fields': ('description_uz_latin', 'description_ru')
        }),
        ('Настройки', {
            'fields': ('points_cost', 'stock_quantity', 'order', 'is_active')
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(GiftRedemption)
class GiftRedemptionAdmin(NoDeleteAdminMixin, SimpleHistoryAdmin):
    """Админка для получения подарков (CRM)."""
    list_display = [
        'redemption_display', 'telegram_id_display', 'phone_number_display', 'region_display',
        'status_badge', 'user_confirmed_badge', 'requested_at'
    ]
    list_filter = [
        'status', 'gift', 'user_confirmed', 'user__user_type', 'user__region__code',
        ('requested_at', DateTimeRangeFilterBuilder(title='Дата запроса (диапазон)')),
    ]
    search_fields = ['user__username', 'user__first_name', 'user__telegram_id', 'user__phone_number',
                     'gift__name_uz_latin', 'gift__name_ru']
    readonly_fields = ['user', 'gift', 'region_display', 'requested_at', 'confirmed_at']
    list_per_page = 50
    date_hierarchy = 'requested_at'

    def redemption_display(self, obj):
        """Отображает информацию о заказе."""
        gift_name = obj.gift.name_uz_latin or obj.gift.name_ru or 'Подарок'
        return format_html(
            '<div style="line-height: 1.6;">'
            '<strong style="font-size: 16px;">🎁 {}</strong><br>'
            '<span style="color: #718096; font-size: 14px;">👤 {}</span>',
            gift_name,
            obj.user.first_name or f"ID: {obj.user.telegram_id}"
        )

    redemption_display.short_description = 'Заказ'
    redemption_display.admin_order_field = 'gift__name_uz_latin'

    def telegram_id_display(self, obj):
        """Отображает Telegram ID пользователя."""
        return format_html(
            '<span style="font-family: monospace; color: #3b82f6; font-weight: 600;">{}</span>',
            obj.user.telegram_id
        )

    telegram_id_display.short_description = 'Telegram ID'
    telegram_id_display.admin_order_field = 'user__telegram_id'

    def phone_number_display(self, obj):
        """Отображает номер телефона пользователя."""
        from .utils import format_phone_uz
        if obj.user.phone_number:
            return format_html(
                '<span style="font-family: monospace; color: #10b981; font-weight: 600;">📞 {}</span>',
                format_phone_uz(obj.user.phone_number)
            )
        return format_html('<span style="color: #9ca3af;">-</span>')

    phone_number_display.short_description = 'Телефон'
    phone_number_display.admin_order_field = 'user__phone_number'

    def region_display(self, obj):
        """Отображает регион пользователя."""
        region_name = obj.user.get_region_display('ru')
        if region_name:
            return format_html(
                '<span style="background: #e0e7ff; color: #3730a3; padding: 4px 12px; border-radius: 12px; '
                'font-size: 12px; font-weight: 600;">📍 {}</span>',
                region_name
            )
        return format_html('<span style="color: #9ca3af;">-</span>')

    region_display.short_description = 'Регион'
    region_display.admin_order_field = 'user__region__code'

    def status_badge(self, obj):
        """Отображает статус заказа."""
        colors = {
            'pending': ('#fff3cd', '#856404', '⏳'),
            'approved': ('#d4edda', '#155724', '✅'),
            'sent': ('#dbeafe', '#1e40af', '📦'),
            'completed': ('#d1ecf1', '#0c5460', '✔️'),
            'rejected': ('#f8d7da', '#721c24', '❌'),
            'cancelled_by_user': ('#fce4ec', '#c62828', '🚫'),
            'not_received': ('#fff3e0', '#e65100', '⚠️'),
        }
        bg, text, icon = colors.get(obj.status, ('#f3f4f6', '#374151', '📋'))
        label = dict(obj._meta.get_field('status').choices).get(obj.status, obj.status)
        return format_html(
            '<span style="background: {}; color: {}; padding: 4px 12px; border-radius: 12px; '
            'font-size: 12px; font-weight: 600;">{} {}</span>',
            bg, text, icon, label
        )

    status_badge.short_description = 'Статус'
    status_badge.admin_order_field = 'status'

    def user_confirmed_badge(self, obj):
        """Отображает подтверждение пользователем."""
        if obj.status == 'not_received':
            return format_html(
                '<span style="background: #fee2e2; color: #dc2626; padding: 4px 12px; border-radius: 12px; '
                'font-size: 12px; font-weight: 600;">❌ Подарок не выдан</span>'
            )
        elif obj.user_confirmed is True:
            return format_html(
                '<span style="background: #d4edda; color: #155724; padding: 4px 12px; border-radius: 12px; '
                'font-size: 12px; font-weight: 600;">✅ Подтверждено</span>'
            )
        elif obj.user_confirmed is False and obj.status != 'not_received':
            return format_html(
                '<span style="background: #fff3cd; color: #856404; padding: 4px 12px; border-radius: 12px; '
                'font-size: 12px; font-weight: 600;">⚠️ Не подтверждено</span>'
            )
        return format_html(
            '<span style="background: #f3f4f6; color: #6b7280; padding: 4px 12px; border-radius: 12px; '
            'font-size: 12px; font-weight: 600;">-</span>'
        )

    user_confirmed_badge.short_description = 'Подтверждение'
    user_confirmed_badge.admin_order_field = 'user_confirmed'

    fieldsets = (
        ('Информация о запросе', {
            'fields': ('user', 'gift', 'region_display', 'requested_at')
        }),
        ('Обработка', {
            'fields': ('status', 'admin_notes')
        }),
        ('Подтверждение пользователем', {
            'fields': ('user_confirmed', 'user_comment', 'confirmed_at')
        }),
    )

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        """Ограничивает выбор статусов в зависимости от роли пользователя."""
        if db_field.name == 'status':
            # Проверяем, имеет ли пользователь пермишн агента
            is_agent = request.user.has_perm('core.change_status_agent')
            # Проверяем, имеет ли пользователь пермишн call center
            is_call_center = request.user.has_perm('core.change_status_call_center')
            
            if not request.user.is_superuser:
                choices = list(GiftRedemption.STATUS_CHOICES)

                # Агенты видят только 'sent' и 'completed'
                if is_agent:
                    filtered_choices = [choice for choice in choices if choice[0] in ['sent', 'completed']]
                    kwargs['choices'] = filtered_choices
                # Call Center видит операционные статусы обработки заявки
                elif is_call_center:
                    filtered_choices = [choice for choice in choices if choice[0] in
                                        ['pending', 'approved', 'sent', 'completed', 'rejected', 'cancelled_by_user']
                                        ]
                kwargs['choices'] = filtered_choices

        return super().formfield_for_dbfield(db_field, request, **kwargs)

    def get_readonly_fields(self, request, obj=None):
        """Управляет readonly полями в зависимости от роли пользователя."""
        readonly = list(super().get_readonly_fields(request, obj))

        if not request.user.is_superuser:
            # Агенты могут изменять только status
            if request.user.has_perm('core.change_status_agent'):
                # Получаем все поля модели
                model_fields = [
                    f.name for f in GiftRedemption._meta.get_fields()
                    if isinstance(f, models.Field) and hasattr(f, 'name')
                ]
                # Делаем все поля readonly кроме status
                for field in model_fields:
                    if field != 'status' and field not in readonly:
                        readonly.append(field)
            # Call Center не может подтверждать получение подарка
            elif request.user.has_perm('core.change_status_call_center'):
                if 'user_confirmed' not in readonly:
                    readonly.append('user_confirmed')

        return readonly

    def save_model(self, request, obj, form, change):
        """Автоматически устанавливает processed_at при изменении статуса и отправляет уведомления."""
        # Проверяем права доступа
        is_agent = request.user.has_perm('core.change_status_agent')

        is_call_center = request.user.has_perm('core.change_status_call_center')
        # Примечание: доступность конкретных статусов управляется списком choices в formfield_for_dbfield.
        
        old_status = None

        if change:
            # Получаем старые значения статуса
            old_obj = GiftRedemption.objects.get(pk=obj.pk)
            old_status = old_obj.status

        # Сохраняем объект
        super().save_model(request, obj, form, change)

        # Инвалидируем кеш баллов при изменении статуса на отмену/отклонение
        if change and 'status' in form.changed_data:
            if obj.status in ['rejected', 'cancelled_by_user', 'not_received']:
                obj.user.invalidate_points_cache()
                obj.user.calculate_points(force=True)

        # Отправляем уведомления после сохранения
        if change:
            import asyncio
            from aiogram import Bot
            from bot.translations import get_text

            async def send_notification():
                try:
                    bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
                    user = obj.user
                    gift_name = obj.gift.get_name(user.language if user else 'uz_latin')

                    # Уведомление об изменении статуса
                    if 'status' in form.changed_data and old_status != obj.status:
                        if obj.status == 'approved':
                            message = get_text(user, 'GIFT_STATUS_APPROVED', gift_name=gift_name)
                        elif obj.status == 'sent':
                            message = get_text(user, 'GIFT_STATUS_SENT', gift_name=gift_name)
                        elif obj.status == 'completed':
                            message = get_text(user, 'GIFT_STATUS_COMPLETED', gift_name=gift_name)
                        elif obj.status == 'rejected':
                            admin_notes = obj.admin_notes or ""
                            # Формируем текст причины в зависимости от языка пользователя
                            if user.language == 'ru':
                                if admin_notes and admin_notes.strip():
                                    admin_notes_text = f"Причина: {admin_notes}"
                                else:
                                    admin_notes_text = "Причина не указана"
                            else:  # uz_latin
                                if admin_notes and admin_notes.strip():
                                    admin_notes_text = f"Sabab: {admin_notes}"
                                else:
                                    admin_notes_text = "Sabab ko'rsatilmagan"
                            message = get_text(user, 'GIFT_STATUS_REJECTED', gift_name=gift_name,
                                               admin_notes=admin_notes_text)
                        else:
                            message = None

                        if message:
                            from core.messaging import send_message_to_user
                            await send_message_to_user(bot, user, message)

                    await bot.session.close()
                except Exception as e:
                    import logging
                    logger = logging.getLogger(__name__)
                    logger.error(f"Ошибка при отправке уведомления о статусе подарка: {e}")

            # Запускаем асинхронную функцию в отдельном потоке
            # Это необходимо, так как Django admin работает в синхронном контексте
            import threading

            def run_async_in_thread():
                """Запускает асинхронную функцию в новом event loop в отдельном потоке."""
                new_loop = asyncio.new_event_loop()
                asyncio.set_event_loop(new_loop)
                try:
                    new_loop.run_until_complete(send_notification())
                finally:
                    new_loop.close()

            thread = threading.Thread(target=run_async_in_thread, daemon=True)
            thread.start()


@admin.register(RegionMessageLog)
class RegionMessageLogAdmin(NoDeleteAdminMixin, admin.ModelAdmin):
    """Логи рассылок по областям (результаты Celery-задач)."""
    list_display = [
        'region_code', 'total', 'sent_count', 'failed_count', 'status',
        'scheduled_at', 'initiated_by', 'created_at', 'completed_at', 'cancel_button',
    ]
    list_filter = ['status', 'region_code', ('created_at', DateTimeRangeFilterBuilder(title='Дата'))]
    readonly_fields = [
        'region_code', 'user_type_filter', 'language_filter',
        'total', 'sent_count', 'failed_count', 'status',
        'initiated_by', 'created_at', 'scheduled_at', 'completed_at',
        'error_message', 'message_text', 'image_storage_path',
    ]
    search_fields = ['region_code', 'error_message', 'message_text']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def get_urls(self):
        urls = super().get_urls()
        custom = [
            path(
                '<int:log_id>/cancel/',
                self.admin_site.admin_view(self.cancel_scheduled_view),
                name='core_regionmessagelog_cancel',
            ),
        ]
        return custom + urls

    def cancel_scheduled_view(self, request, log_id):
        from django.utils import timezone
        try:
            log = RegionMessageLog.objects.get(pk=log_id)
        except RegionMessageLog.DoesNotExist:
            self.message_user(request, 'Запись не найдена', messages.ERROR)
            return redirect('admin:core_regionmessagelog_changelist')
        if log.status != 'pending':
            self.message_user(
                request,
                f'Нельзя отменить рассылку в статусе «{log.get_status_display()}»',
                messages.WARNING,
            )
            return redirect('admin:core_regionmessagelog_changelist')
        log.status = 'cancelled'
        log.completed_at = timezone.now()
        log.save(update_fields=['status', 'completed_at'])
        self.message_user(
            request,
            f'Запланированная рассылка отменена. Если задача уже стартовала в Celery, '
            f'она увидит статус «cancelled» и завершится.',
            messages.SUCCESS,
        )
        return redirect('admin:core_regionmessagelog_changelist')

    def cancel_button(self, obj):
        if obj.status != 'pending':
            return ''
        from django.urls import reverse
        url = reverse('admin:core_regionmessagelog_cancel', args=[obj.pk])
        return format_html(
            '<a href="{}" style="background:#dc3545;color:white;padding:4px 10px;'
            'border-radius:4px;text-decoration:none;font-size:12px;" '
            'onclick="return confirm(\'Отменить запланированную рассылку?\');">✕ Отменить</a>',
            url,
        )

    cancel_button.short_description = 'Отмена'


@admin.register(BroadcastMessage)
class BroadcastMessageAdmin(NoDeleteAdminMixin, SimpleHistoryAdmin):
    """Админка для массовых рассылок (скрыта из меню админки)."""
    list_display = [
        'title', 'status', 'user_type_filter', 'total_users',
        'sent_count', 'failed_count', 'created_at', 'completed_at', 'send_button'
    ]
    list_filter = [
        'status', 'user_type_filter', 'region_filter',
        ('created_at', DateTimeRangeFilterBuilder(title='Дата создания (диапазон)')),
    ]
    search_fields = ['title', 'message_text']
    readonly_fields = [
        'status', 'total_users', 'sent_count', 'failed_count',
        'created_at', 'started_at', 'completed_at'
    ]

    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'message_text', 'image', 'user_type_filter'),
            'description': 'Текст поддерживает HTML: <b>жирный</b>, <i>курсив</i>, <a href="url">ссылка</a>. Эмодзи и стикеры можно вставлять в текст. Фото — опционально.'
        }),
        ("Do'kon bo'yicha filtr", {
            'fields': ('store_filter',),
            'description': "Tanlangan do'kon egasi va uning santeniklariga yuborish. Bo'sh qolsa — filtr qo'llanmaydi.",
        }),
        ('Фильтрация по региону', {
            'fields': ('region_filter',),
            'description': 'Выберите область для фильтрации пользователей. Если не выбрано, сообщение будет отправлено всем пользователям.'
        }),
        ('Статистика', {
            'fields': (
                'status', 'total_users', 'sent_count', 'failed_count',
                'created_at', 'started_at', 'completed_at'
            )
        }),
    )

    actions = ['send_broadcast_action']

    def has_module_permission(self, request):
        """Скрыть модель из меню админки."""
        return False

    def send_button(self, obj):
        """Кнопка отправки рассылки в списке."""
        if obj.status == 'pending':
            from django.urls import reverse
            url = reverse('admin:core_broadcastmessage_send_single', args=[obj.pk])
            return format_html(
                '<a href="{}" style="background: #28a745; color: white; padding: 6px 12px; '
                'border-radius: 4px; text-decoration: none; white-space: nowrap; font-size: 12px;" '
                'onclick="return confirm(\'Отправить рассылку?\');">📤 Отправить</a>',
                url
            )
        elif obj.status == 'sending':
            return format_html(
                '<span style="color: #1e40af; font-size: 12px;">🔄 Отправляется...</span>'
            )
        elif obj.status == 'completed':
            return format_html(
                '<span style="color: #155724; font-size: 12px;">✅ Отправлено</span>'
            )
        return '-'

    send_button.short_description = 'Действие'

    def get_urls(self):
        """Добавляет кастомные URL."""
        urls = super().get_urls()
        custom_urls = [
            path('<int:broadcast_id>/send/', self.admin_site.admin_view(self.send_single_broadcast_view),
                 name='core_broadcastmessage_send_single'),
        ]
        return custom_urls + urls

    def send_single_broadcast_view(self, request, broadcast_id):
        """Отправка конкретной рассылки."""
        import subprocess

        try:
            broadcast = BroadcastMessage.objects.get(pk=broadcast_id)
        except BroadcastMessage.DoesNotExist:
            self.message_user(request, 'Рассылка не найдена', messages.ERROR)
            return redirect('admin:core_broadcastmessage_changelist')

        if broadcast.status != 'pending':
            self.message_user(request, f'Рассылка "{broadcast.title}" уже была отправлена', messages.WARNING)
            return redirect('admin:core_broadcastmessage_changelist')

        # Предварительно оцениваем количество пользователей
        users_query = TelegramUser.objects.filter(is_active=True)
        if broadcast.user_type_filter:
            users_query = users_query.filter(user_type=broadcast.user_type_filter)
        estimated_users = users_query.count()

        LARGE_BROADCAST_THRESHOLD = 20000

        if estimated_users >= LARGE_BROADCAST_THRESHOLD:
            try:
                from core.tasks import send_broadcast_chained
                send_broadcast_chained.delay(broadcast.id)
                self.message_user(request,
                                  f'Рассылка "{broadcast.title}" запущена через Celery ({estimated_users} пользователей)',
                                  messages.SUCCESS)
            except Exception as e:
                self.message_user(request, f'Ошибка: {e}', messages.ERROR)
        else:
            try:
                subprocess.Popen(['python', 'manage.py', 'send_broadcast', str(broadcast.id)])
                self.message_user(request, f'Рассылка "{broadcast.title}" запущена', messages.SUCCESS)
            except Exception as e:
                self.message_user(request, f'Ошибка: {e}', messages.ERROR)

        return redirect('admin:core_broadcastmessage_changelist')

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        """Добавляет опцию 'Всем' в фильтр по типу пользователя."""
        if db_field.name == 'user_type_filter':
            # Получаем текущие choices из модели
            from core.models import TelegramUser
            choices = list(TelegramUser.USER_TYPE_CHOICES)
            # Добавляем опцию "Всем" в начало списка
            choices.insert(0, ('', 'Всем'))
            kwargs['choices'] = choices
            kwargs['required'] = False
        return super().formfield_for_dbfield(db_field, request, **kwargs)

    def send_broadcast_action(self, request, queryset):
        """Действие для отправки рассылки."""
        import subprocess
        from django.contrib import messages

        for broadcast in queryset:
            if broadcast.status != 'pending':
                self.message_user(
                    request,
                    f'Рассылка "{broadcast.title}" уже была отправлена',
                    level=messages.WARNING
                )
                continue

            # Определяем, использовать ли Celery для больших рассылок
            LARGE_BROADCAST_THRESHOLD = 20000  # Порог для использования Celery

            # Предварительно оцениваем количество пользователей
            from core.models import TelegramUser
            users_query = TelegramUser.objects.filter(is_active=True)
            if broadcast.user_type_filter:
                users_query = users_query.filter(user_type=broadcast.user_type_filter)

            estimated_users = users_query.count()

            # Если пользователей много, используем Celery
            if estimated_users >= LARGE_BROADCAST_THRESHOLD:
                try:
                    from core.tasks import send_broadcast_chained
                    send_broadcast_chained.delay(broadcast.id)
                    self.message_user(
                        request,
                        f'Рассылка "{broadcast.title}" запущена через Celery ({estimated_users} пользователей)',
                        level=messages.SUCCESS
                    )
                except Exception as e:
                    self.message_user(
                        request,
                        f'Ошибка при запуске рассылки через Celery: {e}',
                        level=messages.ERROR
                    )
            else:
                # Для небольших рассылок используем обычную команду
                try:
                    subprocess.Popen([
                        'python', 'manage.py', 'send_broadcast', str(broadcast.id)
                    ])
                    self.message_user(
                        request,
                        f'Рассылка "{broadcast.title}" запущена',
                        level=messages.SUCCESS
                    )
                except Exception as e:
                    self.message_user(
                        request,
                        f'Ошибка при запуске рассылки: {e}',
                        level=messages.ERROR
                    )

    send_broadcast_action.short_description = 'Отправить выбранные рассылки'


@admin.register(Promotion)
class PromotionAdmin(NoDeleteAdminMixin, SimpleHistoryAdmin):
    """Админка для акций — admin paneldan yashirilgan (user talab).
    Model DB da saqlanadi (data safety), faqat sidebar'dan yo'qoladi.
    """

    def has_module_permission(self, request):
        return False

    list_display = [
        'image_preview', 'title', 'date_display', 'order', 'is_active', 'status_badge', 'created_at'
    ]
    list_filter = [
        'is_active',
        ('created_at', DateTimeRangeFilterBuilder(title='Дата создания (диапазон)')),
        ('date', DateRangeFilterBuilder(title='Дата акции (диапазон)')),
    ]
    search_fields = ['title']
    list_editable = ['order', 'is_active']
    ordering = ['order', '-created_at']
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'image', 'date', 'order', 'is_active')
        }),
        ('Системная информация', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    readonly_fields = ['created_at', 'updated_at']

    def image_preview(self, obj):
        """Превью изображения акции."""
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width: 100px; max-height: 100px; object-fit: cover; border-radius: 8px;" />',
                obj.image.url
            )
        return '-'

    image_preview.short_description = 'Rasm'

    def date_display(self, obj):
        """Отображает дату в формате DD.MM.YYYY."""
        if obj.date:
            return obj.date.strftime('%d.%m.%Y')
        return '-'

    date_display.short_description = 'Sana'
    date_display.admin_order_field = 'date'

    def status_badge(self, obj):
        """Отображает статус активности."""
        if obj.is_active:
            return format_html(
                '<span style="background: #10B981; color: white; padding: 4px 8px; border-radius: 4px; font-size: 11px;">Faol</span>'
            )
        return format_html(
            '<span style="background: #EF4444; color: white; padding: 4px 8px; border-radius: 4px; font-size: 11px;">Nofaol</span>'
        )

    status_badge.short_description = 'Holat'



@admin.register(MonthlyPromoTicket)
class MonthlyPromoTicketAdmin(NoDeleteAdminMixin, SimpleHistoryAdmin):
    """Билеты месячного розыгрыша — admin paneldan yashirilgan
    (user talab: olib tashlash). Model DB da saqlanadi, lekin yangi
    biletlar yaratilmaydi (assign_monthly_ticket bot dan o'chirildi).
    """

    def has_module_permission(self, request):
        return False

    list_display = [
        'month', 'user_type', 'order', 'qr_code_link',
        'user_link', 'telegram_id', 'scanned_at', 'created_at',
    ]
    list_filter = [
        'month',
        'user_type',
        ('scanned_at', DateTimeRangeFilterBuilder(title='Сканирование (диапазон)')),
    ]
    search_fields = [
        'qr_code__code', 'qr_code__serial_number',
        'user__telegram_id', 'user__username', 'user__first_name', 'user__phone_number',
    ]
    ordering = ['-month', 'user_type', 'order']
    readonly_fields = ['created_at', 'scanned_at']
    list_per_page = 50
    date_hierarchy = 'month'
    raw_id_fields = ['qr_code', 'user']

    def qr_code_link(self, obj):
        try:
            url = reverse('admin:core_qrcode_change', args=[obj.qr_code_id])
            return format_html('<a href="{}">{}</a>', url, obj.qr_code.code)
        except Exception:
            return str(obj.qr_code_id)

    qr_code_link.short_description = 'QR-promokod'
    qr_code_link.admin_order_field = 'qr_code__code'

    def user_link(self, obj):
        try:
            url = reverse('admin:core_telegramuser_change', args=[obj.user_id])
            label = obj.user.first_name or obj.user.username or str(obj.user.telegram_id)
            return format_html('<a href="{}">{}</a>', url, label)
        except Exception:
            return str(obj.user_id)

    user_link.short_description = 'Пользователь'
    user_link.admin_order_field = 'user__first_name'

    def telegram_id(self, obj):
        return obj.user.telegram_id

    telegram_id.short_description = 'Telegram ID'
    telegram_id.admin_order_field = 'user__telegram_id'


@admin.register(PrivacyPolicy)
class PrivacyPolicyAdmin(NoDeleteAdminMixin, SimpleHistoryAdmin):
    """Админка для политики конфиденциальности."""
    list_display = ['is_active', 'updated_at', 'created_at', 'has_pdf_files']
    list_display_links = ['is_active', 'updated_at', 'created_at', 'has_pdf_files']
    list_filter = [
        'is_active',
    ]
    fieldsets = (
        ('Узбекский язык (Латиница)', {
            'fields': ('pdf_uz_latin',),
        }),
        ('Русский язык', {
            'fields': ('pdf_ru',),
        }),
        ('Настройки', {
            'fields': ('is_active',),
        }),
        ('Системная информация', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ['created_at', 'updated_at']

    def has_pdf_files(self, obj):
        """Показывает, загружены ли PDF файлы."""
        if not obj:
            return '-'
        pdfs = []
        if obj.pdf_uz_latin:
            pdfs.append('UZ (Lat)')
        if obj.pdf_ru:
            pdfs.append('RU')
        return ', '.join(pdfs) if pdfs else 'Нет PDF'

    has_pdf_files.short_description = 'Загруженные PDF'

    def has_add_permission(self, request):
        """Разрешаем создание только для superuser (Call Center не может создавать QR коды)."""
        # Только superuser может создавать QR коды
        # Call Center не может создавать QR коды, даже если у них есть permission generate_qrcodes
        return request.user.is_superuser


@admin.register(AdminContactSettings)
class AdminContactSettingsAdmin(NoDeleteAdminMixin, SimpleHistoryAdmin):
    """Админка для настроек контакта администратора."""
    list_display = ['contact_type_display', 'contact_value_display', 'is_active', 'updated_at']
    list_filter = [
        'contact_type', 'is_active',
        ('updated_at', DateTimeRangeFilterBuilder(title='Дата обновления (диапазон)')),
    ]
    search_fields = ['contact_value']
    fields = ['contact_type', 'contact_value', 'is_active']
    readonly_fields = ['created_at', 'updated_at']

    def contact_type_display(self, obj):
        """Отображает тип контакта с иконкой."""
        icons = {
            'telegram': '💬',
            'phone': '📞',
            'link': '🔗',
        }
        icon = icons.get(obj.contact_type, '📋')
        return format_html('{} {}', icon, obj.get_contact_type_display())

    contact_type_display.short_description = 'Kontakt turi'

    def contact_value_display(self, obj):
        """Отображает значение контакта с предпросмотром URL."""
        url = obj.get_contact_url()
        if url:
            return format_html(
                '<strong>{}</strong><br><a href="{}" target="_blank" style="color: #2064AE; font-size: 12px;">{}</a>',
                obj.contact_value, url, url
            )
        return obj.contact_value

    contact_value_display.short_description = 'Kontakt qiymati'

    def has_add_permission(self, request):
        """Разрешаем создание только для superuser."""
        return request.user.is_superuser


@admin.register(VideoInstruction)
class VideoInstructionAdmin(NoDeleteAdminMixin, SimpleHistoryAdmin):
    """Админка для видео инструкций. 4 видео: сантехники (UZ/RU) и предприниматели (UZ/RU)."""
    list_display = ['video_seller_preview', 'file_id_status', 'is_active', 'updated_at']
    list_filter = [
        'is_active',
        ('updated_at', DateTimeRangeFilterBuilder(title='Дата обновления (диапазон)')),
    ]
    fieldsets = (
        ('Video — Santeniklarlar', {
            'fields': ('video_seller_uz', 'thumb_seller_uz', 'video_seller_ru', 'thumb_seller_ru')
        }),
        ('Telegram file_id (avtomatik)', {
            'fields': ('file_id_seller_uz', 'file_id_seller_ru'),
            'description': 'File_id avtomatik to\'ldiriladi. Thumbnail — JPEG max 320x320, 200KB.'
        }),
        ('Sozlamalar', {
            'fields': ('is_active',)
        }),
        ('Sana', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    readonly_fields = ['created_at', 'updated_at', 'file_id_seller_uz', 'file_id_seller_ru']

    def video_seller_preview(self, obj):
        uz = '✅' if obj.video_seller_uz else '❌'
        ru = '✅' if obj.video_seller_ru else '❌'
        return format_html('<span>🛒 Santenik: UZ {} | RU {}</span>', uz, ru)

    video_seller_preview.short_description = 'Video'

    def file_id_status(self, obj):
        return format_html(
            '🛒 UZ{} RU{}',
            '✅' if obj.file_id_seller_uz else '❌',
            '✅' if obj.file_id_seller_ru else '❌',
        )

    file_id_status.short_description = 'File ID'

    def has_add_permission(self, request):
        """Разрешаем создание только для superuser."""
        return request.user.is_superuser

    def save_model(self, request, obj, form, change):
        """При сохранении деактивируем другие активные инструкции, если эта активна."""
        if obj.is_active:
            # Деактивируем все другие активные инструкции
            VideoInstruction.objects.filter(is_active=True).exclude(pk=obj.pk if obj.pk else None).update(
                is_active=False)
        super().save_model(request, obj, form, change)


# JIP — yangi modellar uchun admin
class QRCodeBatchInline(admin.TabularInline):
    """Do'kon sahifasida batch'larni inline ko'rsatish."""
    model = QRCodeBatch
    extra = 0
    fields = ['name', 'quantity', 'points_per_code', 'status', 'delivery_status', 'activation_rate_display', 'zip_download']
    readonly_fields = ['name', 'status', 'activation_rate_display', 'zip_download']
    show_change_link = True
    ordering = ['-created_at']
    max_num = 20

    def activation_rate_display(self, obj):
        rate = obj.activation_rate()
        color = '#16a34a' if rate >= 50 else ('#ca8a04' if rate >= 20 else '#dc2626')
        scanned = obj.qr_codes.filter(is_scanned=True).count()
        return format_html(
            '<b style="color:{};">{}%</b> <small>({}/{})</small>',
            color, rate, scanned, obj.quantity
        )
    activation_rate_display.short_description = 'Aktivatsiya'

    def zip_download(self, obj):
        if obj.zip_file:
            return format_html('<a href="{}" target="_blank">⬇ ZIP</a>', obj.zip_file.url)
        if obj.status == 'inactive':
            return '⏳ Generatsiya...'
        return '—'
    zip_download.short_description = 'ZIP'

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Store)
class StoreAdmin(SimpleHistoryAdmin):
    """JIP: Do'kon admin — admin menyusidan yashirilgan."""
    list_display = [
        'name', 'region', 'district', 'owner_display', 'phone_display',
        'batches_count', 'qr_codes_stats', 'commission_percent', 'is_active', 'created_at',
    ]
    list_filter = ['is_active', 'region', 'district']
    search_fields = ['name', 'legal_name', 'phone', 'owner__first_name', 'owner__phone_number']
    autocomplete_fields = ['region', 'district', 'owner']
    readonly_fields = ['created_at', 'updated_at', 'store_statistics']
    list_per_page = 50

    def has_module_permission(self, request):
        return False
    inlines = [QRCodeBatchInline]

    fieldsets = (
        ('📊 Statistika', {
            'fields': ('store_statistics',),
        }),
        ("Asosiy ma'lumotlar", {
            'fields': ('name', 'legal_name', 'phone', 'address', 'logo'),
        }),
        ('Joylashuv', {
            'fields': ('region', 'district', 'latitude', 'longitude'),
        }),
        ('Egasi (sotuvchi)', {
            'fields': ('owner',),
            'description': "Telefon raqami orqali avtomatik biriktirilishi mumkin.",
        }),
        ('Komissiya va shartnoma', {
            'fields': ('commission_percent', 'contract_signed_at'),
        }),
        ('Holat', {
            'fields': ('is_active', 'created_at', 'updated_at'),
        }),
    )

    def store_statistics(self, obj):
        if not obj.pk:
            return '—'
        total_qr = obj.total_qr_codes()
        scanned_qr = obj.scanned_qr_codes()
        rate = obj.activation_rate()
        batches = obj.batches.count()
        santeniks = obj.qr_codes.filter(
            is_scanned=True, scanned_by__isnull=False
        ).values('scanned_by').distinct().count()
        return format_html(
            '''<table style="border-collapse:collapse;min-width:400px;">
            <tr>
              <td style="padding:8px 16px 8px 0;"><b>Jami QR kodlar:</b></td>
              <td style="padding:8px 0;font-size:16px;font-weight:700;">{}</td>
            </tr>
            <tr>
              <td style="padding:8px 16px 8px 0;"><b>Skanlanganlar:</b></td>
              <td style="padding:8px 0;font-size:16px;font-weight:700;color:#16a34a;">{}</td>
            </tr>
            <tr>
              <td style="padding:8px 16px 8px 0;"><b>Aktivatsiya darajasi:</b></td>
              <td style="padding:8px 0;font-size:16px;font-weight:700;color:#2563eb;">{}%</td>
            </tr>
            <tr>
              <td style="padding:8px 16px 8px 0;"><b>Partiyalar soni:</b></td>
              <td style="padding:8px 0;">{}</td>
            </tr>
            <tr>
              <td style="padding:8px 16px 8px 0;"><b>Santeniklarlar soni:</b></td>
              <td style="padding:8px 0;">{}</td>
            </tr>
            </table>''',
            total_qr, scanned_qr, rate, batches, santeniks
        )
    store_statistics.short_description = "Do'kon statistikasi"

    def owner_display(self, obj):
        from .utils import format_phone_uz
        if obj.owner_id:
            phone = format_phone_uz(obj.owner.phone_number) if obj.owner.phone_number else '-'
            return f"{obj.owner.first_name or ''} ({phone})"
        return format_html('<span style="color:#c00;">— biriktirilmagan —</span>')
    owner_display.short_description = 'Egasi'

    def phone_display(self, obj):
        from .utils import format_phone_uz
        return format_phone_uz(obj.phone) if obj.phone else '-'
    phone_display.short_description = 'Telefon'
    phone_display.admin_order_field = 'phone'

    def batches_count(self, obj):
        count = obj.batches.count()
        url = reverse('admin:core_qrcodebatch_changelist') + f'?store__id__exact={obj.pk}'
        return format_html('<a href="{}">{} batch</a>', url, count)
    batches_count.short_description = "Partiyalar"

    def qr_codes_stats(self, obj):
        total = obj.total_qr_codes()
        scanned = obj.scanned_qr_codes()
        rate = obj.activation_rate()
        color = '#16a34a' if rate >= 50 else ('#ca8a04' if rate >= 20 else '#dc2626')
        return format_html(
            '<span style="color:{};font-weight:600;">{}%</span> <small>({}/{})</small>',
            color, rate, scanned, total
        )
    qr_codes_stats.short_description = 'Aktivatsiya'


def _notify_seller_new_batch(seller_id: int, batch_name: str, qty: int, points: int) -> None:
    """Yangi partiya yaratilganda sotuvchiga Telegram orqali xabar yuboradi.

    Sync funksiya — Telegram API ni urllib bilan to'g'ridan-to'g'ri chaqiradi
    (aiogram event loop muammosiz). Background thread'da ishlaydi.
    """
    import threading, urllib.request, urllib.parse, json
    from django.conf import settings

    def _send():
        try:
            user = TelegramUser.objects.filter(pk=seller_id).first()
            if not user or not user.telegram_id:
                return
            token = getattr(settings, 'TELEGRAM_BOT_TOKEN', '')
            if not token:
                return
            lang_ru = (user.language or 'uz_latin') == 'ru'
            if lang_ru:
                text = (
                    f"🎉 <b>Новая партия!</b>\n\n"
                    f"📦 <code>{batch_name}</code>\n"
                    f"🔢 Количество: <b>{qty}</b> карт\n"
                    f"💰 Начислено: <b>+{points:,}</b> баллов".replace(',', ' ')
                )
            else:
                text = (
                    f"🎉 <b>Yangi partiya!</b>\n\n"
                    f"📦 <code>{batch_name}</code>\n"
                    f"🔢 Miqdor: <b>{qty}</b> karta\n"
                    f"💰 Qo'shildi: <b>+{points:,}</b> ball".replace(',', ' ')
                )
            url = f'https://api.telegram.org/bot{token}/sendMessage'
            data = urllib.parse.urlencode({
                'chat_id': user.telegram_id,
                'text': text,
                'parse_mode': 'HTML',
            }).encode()
            req = urllib.request.Request(url, data=data)
            urllib.request.urlopen(req, timeout=8)
        except Exception:
            import logging
            logging.getLogger(__name__).exception("_notify_seller_new_batch background failed")

    threading.Thread(target=_send, daemon=True).start()


@admin.register(QRCodeBatch)
class QRCodeBatchAdmin(SimpleHistoryAdmin):
    """Promokod yaratish tarixi — har generatsiya bitta yozuv.

    Yangi tizim:
    - Admin "Promo-kodni yaratish" tugmasi orqali N ta promokod yaratadi
    - Har generatsiya bitta QRCodeBatch yozuvi sifatida log qilinadi
    - .xlsx fayl avtomatik yaratiladi va batch'ga biriktiriladi
    - Sotuvchiga biriktirish — bu yerda emas, SellerAdmin → Partiyalar
    """

    list_display = [
        'id_col', 'quantity_col', 'points_col', 'status_col',
        'scanned_col', 'activation_col',
        'created_by', 'created_at', 'completed_at', 'xlsx_link',
    ]
    list_filter = ['status', ('created_at', DateTimeRangeFilterBuilder(title='Yaratilgan sana'))]
    search_fields = ['name']
    ordering = ['-created_at']
    list_per_page = 50
    date_hierarchy = 'created_at'

    readonly_fields = [
        'name', 'quantity', 'points_per_code', 'status',
        'created_at', 'completed_at', 'created_by',
        'zip_file', 'error_message', 'batch_qr_history_link',
    ]

    fieldsets = (
        ('Generatsiya', {
            'fields': ('name', 'quantity', 'points_per_code', 'status',
                       'created_by', 'created_at', 'completed_at'),
        }),
        ('Fayl', {
            'fields': ('zip_file', 'error_message'),
        }),
        ('Promokodlar', {
            'fields': ('batch_qr_history_link',),
        }),
    )

    def has_add_permission(self, request):
        # Faqat "Promo-kodni yaratish" sahifasi orqali yaratiladi
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def id_col(self, obj):
        return format_html('<strong>#{}</strong>', obj.id)
    id_col.short_description = 'ID'

    def quantity_col(self, obj):
        return f'{obj.quantity}'
    quantity_col.short_description = 'Miqdor'
    quantity_col.admin_order_field = 'quantity'

    def points_col(self, obj):
        return format_html(
            '<span style="color:#1d4ed8;font-weight:600;">{} ball</span>',
            obj.points_per_code,
        )
    points_col.short_description = 'Ball/QR'

    def status_col(self, obj):
        color = '#16a34a' if obj.status == 'active' else '#9ca3af'
        return format_html(
            '<span style="background:{};color:#fff;padding:2px 10px;border-radius:10px;font-size:11px;">{}</span>',
            color, obj.get_status_display(),
        )
    status_col.short_description = 'Holat'

    def scanned_col(self, obj):
        scanned = obj.qr_codes.filter(is_scanned=True).count()
        url = reverse('admin:core_qrcode_changelist') + f'?batch__id__exact={obj.pk}&is_scanned__exact=1'
        return format_html('<a href="{}">{} ta</a>', url, scanned)
    scanned_col.short_description = 'Aktivlashtirilgan'

    def activation_col(self, obj):
        total = obj.qr_codes.count()
        scanned = obj.qr_codes.filter(is_scanned=True).count()
        pct = round((scanned / total * 100), 1) if total else 0
        color = '#16a34a' if pct >= 50 else ('#ca8a04' if pct >= 20 else '#dc2626')
        return format_html(
            '<span style="color:{};font-weight:600;">{}%</span>',
            color, pct,
        )
    activation_col.short_description = 'Aktivatsiya'

    def xlsx_link(self, obj):
        # On-demand xlsx (productionda media files servirovat qilinmaydi)
        if obj.pk and obj.qr_codes.exists():
            # Top-level URL — admin namespace'da emas
            url = f'/admin/qrcodebatch/{obj.pk}/xlsx/'
            return format_html(
                '<a href="{}" target="_blank" '
                'style="background:#16a34a;color:#fff;padding:5px 12px;border-radius:6px;'
                'text-decoration:none;font-size:12px;white-space:nowrap;">📊 .xlsx</a>',
                url,
            )
        return format_html('<span style="color:#9ca3af;">—</span>')
    xlsx_link.short_description = 'Yuklab olish'

    def batch_qr_history_link(self, obj):
        if not obj.pk:
            return '—'
        url = reverse('admin:core_qrcode_changelist') + f'?batch__id__exact={obj.pk}'
        return format_html(
            '<a href="{}" class="button">📋 {} ta promokodni ko\'rish</a>',
            url, obj.qr_codes.count(),
        )
    batch_qr_history_link.short_description = 'Promokodlar ro\'yxati'

    @admin.action(description="📦 ZIP generatsiya qilish (Celery)")
    def action_generate_zip(self, request, queryset):
        from .tasks import generate_batch_zip
        triggered, skipped = 0, 0
        for batch in queryset:
            if batch.status != 'active':
                generate_batch_zip.delay(batch.id)
                triggered += 1
            else:
                skipped += 1
        if triggered:
            self.message_user(request, f"✅ {triggered} ta partiya uchun ZIP generatsiya boshlandi.")
        if skipped:
            self.message_user(request, f"⚠️ {skipped} ta partiya o'tkazildi (allaqachon faollashtirilgan).", level='warning')

    @admin.action(description="✅ Faollashtirish")
    def action_mark_active(self, request, queryset):
        now = timezone.now()
        count = queryset.update(status='active', delivery_status='active', delivered_at=now)
        self.message_user(request, f"✅ {count} ta partiya faollashtirildi.")

    @admin.action(description="🚫 Faollashtirilmagan deb belgilash")
    def action_mark_inactive(self, request, queryset):
        count = queryset.update(status='inactive', delivery_status='inactive')
        self.message_user(request, f"✅ {count} ta partiya faollashtirilmagan deb belgilandi.")

    def save_model(self, request, obj, form, change):
        import logging
        import traceback
        logger = logging.getLogger(__name__)
        is_new = not obj.pk
        try:
            from .tasks import generate_batch_zip, _do_generate_batch_zip
            if not obj.created_by_id:
                obj.created_by = request.user
            obj.points_per_code = 50
            # Generate name BEFORE first save (seller asosida — store endi optional)
            if is_new and not obj.name:
                if obj.seller_id:
                    obj.name = QRCodeBatch.generate_name(seller=obj.seller)
                elif obj.store_id:
                    obj.name = QRCodeBatch.generate_name(store=obj.store)
            super().save_model(request, obj, form, change)
        except Exception as exc:
            tb = traceback.format_exc()
            logger.error("QRCodeBatch save_model PRE/SAVE xato: %s\n%s", exc, tb)
            self.message_user(
                request,
                f"❌ Partiya saqlashda xato: {type(exc).__name__}: {exc}",
                level='error',
            )
            return
        if is_new and obj.seller_id:
            try:
                bonus_points = obj.quantity * 50
                from django.db.models import F as DbF
                TelegramUser.objects.filter(pk=obj.seller_id).update(points=DbF('points') + bonus_points)
                SellerPointsTransaction.objects.create(
                    seller=obj.seller,
                    store=None,  # Store endi kerak emas — ball to'g'ridan-to'g'ri sotuvchiga
                    transaction_type='bonus',
                    points=bonus_points,
                    note=f"Partiya '{obj.name}' yaratildi ({obj.quantity} ta × 50 ball)",
                    created_by=request.user,
                )
                obj.seller.invalidate_points_cache()
                self.message_user(
                    request,
                    f"✅ '{obj.name}' batch yaratildi. Sotuvchiga {bonus_points:,} ball qo'shildi.",
                )
                # Sotuvchiga Telegram orqali xabar yuborish (background)
                try:
                    _notify_seller_new_batch(obj.seller_id, obj.name, obj.quantity, bonus_points)
                except Exception as exc:
                    logger.warning("Seller TG notify failed: %s", exc)
            except Exception as exc:
                tb = traceback.format_exc()
                logger.error("SellerPointsTransaction xato: %s\n%s", exc, tb)
                self.message_user(
                    request,
                    f"⚠️ Partiya yaratildi, ammo ball qo'shishda xato: {type(exc).__name__}: {exc}",
                    level='warning',
                )
        elif is_new:
            self.message_user(request, f"✅ '{obj.name}' batch yaratildi.")
        if is_new:
            try:
                generate_batch_zip.delay(obj.id)
            except Exception as exc:
                logger.warning("Celery delay() xato (thread fallback): %s", exc)
                try:
                    import threading
                    t = threading.Thread(target=_do_generate_batch_zip, args=(obj,), daemon=True)
                    t.start()
                except Exception as exc2:
                    logger.error("Thread fallback ham xato: %s", exc2)
                    self.message_user(
                        request,
                        f"⚠️ ZIP generatsiyasi boshlanmadi: {type(exc2).__name__}: {exc2}",
                        level='warning',
                    )


@admin.register(SellerPointsTransaction)
class SellerPointsTransactionAdmin(SimpleHistoryAdmin):
    """JIP: Eski tranzaksiya tizimi — sidebar dan yashirilgan."""

    def has_module_permission(self, request):
        return False

    list_display = ['created_at', 'seller', 'transaction_type', 'points', 'sales_amount_usd', 'created_by']
    list_filter = ['transaction_type', 'created_at']
    search_fields = ['seller__first_name', 'seller__phone_number', 'note']
    autocomplete_fields = ['seller']
    readonly_fields = ['created_at', 'created_by']
    list_per_page = 50

    fieldsets = (
        ('Sotuvchi', {
            'fields': ('seller',),
        }),
        ('Tranzaksiya', {
            'fields': ('transaction_type', 'points', 'sales_amount_usd'),
        }),
        ('Davr va izoh', {
            'fields': ('period_start', 'period_end', 'note'),
        }),
        ('Audit', {
            'fields': ('created_by', 'created_at'),
        }),
    )

    def save_model(self, request, obj, form, change):
        if not obj.created_by_id:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
        # Sotuvchining cached `points` ni invalidate qilamiz
        if obj.seller_id:
            obj.seller.invalidate_points_cache()
            obj.seller.calculate_points(force=True)


# Кастомная админка для дашборда
admin.site.site_header = 'JIP — Sodiqlik dasturi'
admin.site.site_title = 'JIP Admin'
admin.site.index_title = 'Boshqaruv paneli'


@admin.register(MonthlyReminderSettings)
class MonthlyReminderSettingsAdmin(admin.ModelAdmin):
    """Singleton-настройки ежемесячного напоминания (1-е число)."""
    list_display = ['__str__', 'is_active', 'time_of_day', 'updated_at']
    fieldsets = (
        ('Параметры рассылки', {
            'fields': ('is_active', 'time_of_day'),
            'description': '1-го числа каждого месяца в указанное время сообщение получат пользователи, которые ещё не выбрали роль или не завершили регистрацию.',
        }),
        ('Текст сообщения', {
            'fields': ('text_uz_latin', 'text_ru', 'image'),
            'description': 'Поддерживается HTML: <b>жирный</b>, <i>курсив</i>, <a href="…">ссылка</a>. Если загружена картинка — текст идёт как подпись.',
        }),
    )
    readonly_fields = ('updated_at',)

    def has_add_permission(self, request):
        # Singleton — добавить можно только если ещё нет ни одной записи.
        return not MonthlyReminderSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        # Если запись существует — сразу открываем её на редактирование.
        obj = MonthlyReminderSettings.objects.first()
        if obj:
            from django.urls import reverse
            return redirect(reverse('admin:core_monthlyremindersettings_change', args=[obj.pk]))
        return super().changelist_view(request, extra_context)


@admin.register(MonthlyReminderLog)
class MonthlyReminderLogAdmin(NoDeleteAdminMixin, admin.ModelAdmin):
    """Логи ежемесячного напоминания (read-only)."""
    list_display = [
        'month_key', 'status', 'total', 'sent_count', 'failed_count',
        'started_at', 'completed_at',
    ]
    list_filter = ['status']
    readonly_fields = [
        'month_key', 'status', 'total', 'sent_count', 'failed_count',
        'started_at', 'completed_at', 'error_message',
    ]
    ordering = ['-started_at']

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


class LiveStreamWinnerInline(admin.TabularInline):
    model = LiveStreamWinner
    extra = 0
    autocomplete_fields = ('user',)
    fields = ('position', 'user', 'user_type_display', 'prize_text_uz_latin', 'prize_text_ru')
    readonly_fields = ('user_type_display',)
    ordering = ('position', 'id')

    def user_type_display(self, obj):
        if not obj or not obj.user_id:
            return '-'
        return obj.user.get_user_type_display() if obj.user.user_type else '-'
    user_type_display.short_description = 'Tur'


@admin.register(LiveStream)
class LiveStreamAdmin(NoDeleteAdminMixin, SimpleHistoryAdmin):
    list_display = ['title_uz_latin', 'scheduled_at', 'is_active', 'state_badge', 'winners_count']
    list_filter = [
        'is_active',
        ('scheduled_at', DateTimeRangeFilterBuilder(title='Дата эфира (диапазон)')),
    ]
    search_fields = ['title_uz_latin', 'title_ru']
    list_editable = ['is_active']
    ordering = ['-scheduled_at']
    date_hierarchy = 'scheduled_at'
    inlines = [LiveStreamWinnerInline]

    fieldsets = (
        ('Основная информация', {
            'fields': (
                'title_uz_latin', 'title_ru',
                'description_uz_latin', 'description_ru',
                'scheduled_at', 'stream_url', 'banner',
                'participants_count', 'is_active',
            )
        }),
        ('Системная информация', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    readonly_fields = ['created_at', 'updated_at']

    def state_badge(self, obj):
        if obj.is_past:
            return format_html(
                '<span style="background:#6B7280;color:white;padding:4px 8px;border-radius:4px;font-size:11px;">O\'tgan</span>'
            )
        return format_html(
            '<span style="background:#10B981;color:white;padding:4px 8px;border-radius:4px;font-size:11px;">Yaqinlashayotgan</span>'
        )
    state_badge.short_description = 'Holat'

    def winners_count(self, obj):
        return obj.winners.count()
    winners_count.short_description = "G'oliblar"


@admin.register(PendingSellerRequest)
class PendingSellerRequestAdmin(admin.ModelAdmin):
    """Tasdiqlanmagan sotuvchi arizalari — admin sidebar dan yashirin.

    User talab: admin panelda zaproslar funksiyasi kere emas.
    Endi sotuvchilar SellerRegistrationCode orqali o'zlarini tasdiqlaydi,
    admin tasdiqlashi kerak emas.
    """

    def has_module_permission(self, request):
        return False

    def has_add_permission(self, request):
        return False

    def has_view_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    list_display = ('user_info', 'phone_number', 'region_name', 'district_name', 'registered_at', 'approval_action')
    list_display_links = ('user_info',)
    readonly_fields = ('telegram_id', 'username', 'first_name', 'last_name', 'phone_number',
                       'latitude', 'longitude', 'language', 'user_type', 'created_at')
    ordering = ('-created_at',)
    search_fields = ('first_name', 'last_name', 'username', 'phone_number')

    fields = ('telegram_id', 'username', 'first_name', 'last_name', 'phone_number',
              'language', 'seller_approved', 'created_at')

    def get_queryset(self, request):
        return TelegramUser.objects.filter(user_type='sotuvchi', seller_approved=False)

    def user_info(self, obj):
        name = f"{obj.first_name or ''} {obj.last_name or ''}".strip() or 'Nomsiz'
        username = f"@{obj.username}" if obj.username else ''
        return format_html(
            '<strong>{}</strong><br><span style="color:#888;font-size:11px">{}</span>',
            name, username
        )
    user_info.short_description = 'Foydalanuvchi'

    def region_name(self, obj):
        return obj.region.name if obj.region else '—'
    region_name.short_description = 'Viloyat'

    def district_name(self, obj):
        return obj.district.name if obj.district else '—'
    district_name.short_description = 'Tuman'

    def registered_at(self, obj):
        return obj.created_at.strftime('%d.%m.%Y %H:%M') if obj.created_at else '—'
    registered_at.short_description = 'Ariza sanasi'

    def approval_action(self, obj):
        url = f'/admin/core/pendingsellerrequest/{obj.pk}/change/'
        return format_html(
            '<a href="{}" style="background:#10B981;color:white;padding:4px 10px;border-radius:4px;font-size:11px;text-decoration:none">✅ Ko\'rib chiqish</a>',
            url
        )
    approval_action.short_description = 'Harakat'


@admin.register(SellerRegistrationCode)
class SellerRegistrationCodeAdmin(admin.ModelAdmin):
    """Eski sotuvchi IDlari — sidebar dan yashirilgan."""

    def has_module_permission(self, request):
        return False

    list_display = ['code_display', 'label', 'status_badge', 'used_by_display', 'used_at', 'created_at']
    list_filter = ['is_used']
    search_fields = ['code', 'label']
    readonly_fields = ['code', 'is_used', 'used_by', 'used_at', 'created_at']
    fields = ['code', 'label', 'is_used', 'used_by', 'used_at', 'created_at']
    ordering = ['-created_at']
    change_list_template = 'admin/core/sellerregistrationcode/change_list.html'

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['generate_url'] = reverse('admin:core_sellerregistrationcode_generate')
        extra_context['total_active'] = SellerRegistrationCode.objects.filter(is_used=False).count()
        extra_context['total_used'] = SellerRegistrationCode.objects.filter(is_used=True).count()
        return super().changelist_view(request, extra_context)

    def get_urls(self):
        urls = super().get_urls()
        extra = [
            path('generate/', self.admin_site.admin_view(self.generate_id_view),
                 name='core_sellerregistrationcode_generate'),
        ]
        return extra + urls

    def generate_id_view(self, request):
        try:
            code_str = SellerRegistrationCode.generate_unique_code()
            obj = SellerRegistrationCode.objects.create(code=code_str)
            self.message_user(
                request,
                format_html('✅ Yangi ID yaratildi: <strong style="font-size:16px;letter-spacing:2px;">{}</strong>', obj.code),
                messages.SUCCESS,
            )
        except Exception as e:
            self.message_user(request, f'Xato: {e}', messages.ERROR)
        return redirect(reverse('admin:core_sellerregistrationcode_changelist'))

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return obj is not None and not obj.is_used

    def code_display(self, obj):
        color = '#888' if obj.is_used else '#fff'
        bg = '#1e1e2e' if not obj.is_used else '#2a2a2a'
        return format_html(
            '<code style="background:{};color:{};padding:4px 10px;border-radius:6px;'
            'font-size:15px;letter-spacing:1px;font-weight:700;'
            'font-family:Menlo,Monaco,Consolas,monospace;display:inline-block;'
            'min-width:120px;text-align:center;">{}</code>',
            bg, color, obj.code
        )
    code_display.short_description = 'ID (8 raqam)'

    def status_badge(self, obj):
        if obj.is_used:
            return format_html(
                '<span style="background:#dc2626;color:white;padding:3px 10px;border-radius:12px;font-size:11px;">✅ Ishlatilgan</span>'
            )
        return format_html(
            '<span style="background:#16a34a;color:white;padding:3px 10px;border-radius:12px;font-size:11px;">🔓 Faol</span>'
        )
    status_badge.short_description = 'Holat'

    def used_by_display(self, obj):
        if not obj.used_by:
            return '—'
        name = obj.used_by.first_name or obj.used_by.username or str(obj.used_by.telegram_id)
        return format_html('<a href="/admin/core/telegramuser/{}/change/">{}</a>', obj.used_by_id, name)
    used_by_display.short_description = 'Kim ishlatdi'


# ════════════════════════════════════════════════════════════════════
# ActivityLog admin — markazlashtirilgan audit log ko'rinishi
# ════════════════════════════════════════════════════════════════════
@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    """Faollik tarixi (audit log) — readonly, faqat ko'rish va filter."""

    list_display = ['timestamp_short', 'who_display', 'action_badge', 'target_link', 'desc_short', 'ip_address']
    list_filter = ['action_type', ('timestamp', DateTimeRangeFilterBuilder(title='Vaqt')), 'target_model']
    search_fields = ['user__username', 'tg_user__first_name', 'tg_user__telegram_id',
                     'target_repr', 'description', 'ip_address']
    readonly_fields = [
        'timestamp', 'user', 'tg_user', 'action_type',
        'target_model', 'target_id', 'target_repr',
        'description', 'metadata_pretty', 'ip_address', 'user_agent',
    ]
    fields = readonly_fields
    list_per_page = 100
    date_hierarchy = 'timestamp'
    ordering = ['-timestamp']

    def has_add_permission(self, request):
        return False  # Log faqat avtomatik yoziladi

    def has_change_permission(self, request, obj=None):
        return False  # Tahrir qilinmaydi

    def has_delete_permission(self, request, obj=None):
        # Faqat superuser eski loglarni o'chirishi mumkin
        return request.user.is_superuser

    def timestamp_short(self, obj):
        return obj.timestamp.strftime('%d.%m.%Y %H:%M:%S')
    timestamp_short.short_description = 'Vaqt'
    timestamp_short.admin_order_field = 'timestamp'

    def who_display(self, obj):
        if obj.user_id:
            return format_html(
                '<span style="color:#2563eb;font-weight:600;">👤 {}</span>',
                obj.user.username,
            )
        if obj.tg_user_id:
            name = obj.tg_user.first_name or obj.tg_user.username or str(obj.tg_user.telegram_id)
            return format_html(
                '<span style="color:#7c3aed;font-weight:600;">📱 {}</span>',
                name,
            )
        return format_html('<span style="color:#888;font-style:italic;">tizim</span>')
    who_display.short_description = 'Kim'

    def action_badge(self, obj):
        colors = {
            'login': ('#10b981', '#d1fae5'),
            'logout': ('#64748b', '#f1f5f9'),
            'login_failed': ('#dc2626', '#fee2e2'),
            'create': ('#2563eb', '#dbeafe'),
            'update': ('#d97706', '#fef3c7'),
            'delete': ('#dc2626', '#fee2e2'),
            'backup': ('#7c3aed', '#ede9fe'),
            'export': ('#0891b2', '#cffafe'),
            'webhook': ('#65a30d', '#ecfccb'),
            'admin_action': ('#475569', '#e2e8f0'),
            'error': ('#dc2626', '#fee2e2'),
            'custom': ('#64748b', '#f1f5f9'),
        }
        fg, bg = colors.get(obj.action_type, ('#64748b', '#f1f5f9'))
        label = obj.get_action_type_display()
        return format_html(
            '<span style="background:{};color:{};padding:3px 10px;border-radius:10px;'
            'font-size:11px;font-weight:600;white-space:nowrap;">{}</span>',
            bg, fg, label,
        )
    action_badge.short_description = 'Amal'
    action_badge.admin_order_field = 'action_type'

    def target_link(self, obj):
        if not obj.target_model:
            return '—'
        text = obj.target_repr or f'#{obj.target_id}' if obj.target_id else obj.target_model
        if obj.target_id and obj.target_model:
            # Try to build admin URL
            try:
                url = reverse(
                    f'admin:core_{obj.target_model.lower()}_change',
                    args=[obj.target_id],
                )
                return format_html('<a href="{}">{}</a>', url, text[:50])
            except Exception:
                pass
        return text[:50]
    target_link.short_description = 'Obyekt'

    def desc_short(self, obj):
        text = (obj.description or '').strip()
        if len(text) > 80:
            text = text[:77] + '…'
        return text
    desc_short.short_description = 'Tavsif'

    def metadata_pretty(self, obj):
        if not obj.metadata:
            return '—'
        import json
        try:
            txt = json.dumps(obj.metadata, indent=2, ensure_ascii=False)
        except Exception:
            txt = str(obj.metadata)
        return format_html(
            '<pre style="background:#f8fafc;padding:10px;border-radius:6px;'
            'font-size:11px;max-width:700px;overflow:auto;">{}</pre>',
            txt,
        )
    metadata_pretty.short_description = "Qo'shimcha (JSON)"


# ════════════════════════════════════════════════════════════════════
# Seller admin — Admin tomonidan qo'lda boshqariladigan Sotuvchilar
# ════════════════════════════════════════════════════════════════════

class SellerBatchInline(admin.TabularInline):
    model = SellerBatch
    extra = 1
    can_delete = True
    readonly_fields = ['total_count_col', 'points_col', 'activation_col', 'promos_btn', 'created_at']
    fields = ['promo_from', 'promo_to', 'total_count_col', 'points_col', 'activation_col', 'promos_btn', 'created_at']
    verbose_name = 'Partiya'
    verbose_name_plural = 'Partiyalar'

    def total_count_col(self, obj):
        if not obj.pk:
            return '—'
        return obj.total_count()
    total_count_col.short_description = 'Jami promo'

    def points_col(self, obj):
        if not obj.pk:
            return '—'
        return format_html('<strong style="color:#818cf8;">{}</strong>', f'{obj.points():,}')
    points_col.short_description = 'Ballar'

    def activation_col(self, obj):
        if not obj.pk:
            return '—'
        pct = obj.activation_percent()
        color = '#16a34a' if pct >= 50 else '#ca8a04' if pct >= 20 else '#dc2626'
        return format_html(
            '<span style="color:{};font-weight:700;">{} ({}%)</span>',
            color, obj.activated_count(), f'{pct:.1f}',
        )
    activation_col.short_description = 'Aktivatsiya'

    def promos_btn(self, obj):
        if not obj.pk or not obj.seller_id:
            return '—'
        url = reverse('admin:core_seller_batch_promos', args=[obj.seller_id, obj.pk])
        return format_html(
            '<a href="{}" target="_blank" style="background:#1d4ed8;color:#fff;padding:4px 10px;'
            'border-radius:4px;font-size:11px;text-decoration:none;white-space:nowrap;">📋 Promolar</a>',
            url
        )
    promos_btn.short_description = 'Promolar'


@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    """Admin panel orqali qo'lda boshqariladigan Sotuvchilar."""

    list_display = [
        'name', 'phone', 'region', 'district',
        'total_promos_col', 'total_points_col', 'activation_col', 'created_at',
    ]
    search_fields = ['name', 'phone']
    list_filter = [
        'region',
        ('created_at', DateTimeRangeFilterBuilder(title="Qo'shilgan sana")),
    ]
    autocomplete_fields = ['region', 'district']
    inlines = [SellerBatchInline]
    readonly_fields = ['created_at', 'total_promos_col', 'total_points_col', 'activation_col']
    list_per_page = 50

    fieldsets = (
        ("Asosiy ma'lumot", {
            'fields': (
                'name', 'phone',
                'region', 'district', 'address_other',
                'notes', 'created_at',
                'total_promos_col', 'total_points_col', 'activation_col',
            ),
        }),
    )

    def total_promos_col(self, obj):
        if not obj.pk:
            return '—'
        return format_html('<strong>{}</strong>', obj.total_promos())
    total_promos_col.short_description = 'Jami promokodlar'

    def total_points_col(self, obj):
        if not obj.pk:
            return '—'
        return format_html('<strong style="color:#818cf8;">{}</strong>', f'{obj.total_points():,}')
    total_points_col.short_description = 'Jami ballar'

    def activation_col(self, obj):
        if not obj.pk:
            return '—'
        pct = obj.activation_percent()
        color = '#16a34a' if pct >= 50 else '#ca8a04' if pct >= 20 else '#dc2626'
        return format_html(
            '<span style="color:{};font-weight:700;">{} ta ({}%)</span>',
            color, obj.activated_count(), f'{pct:.1f}',
        )
    activation_col.short_description = 'Aktivatsiya'

    def get_urls(self):
        urls = super().get_urls()
        extra = [
            path(
                '<int:seller_id>/batch/<int:batch_id>/promos/',
                self.admin_site.admin_view(self.batch_promos_view),
                name='core_seller_batch_promos',
            ),
        ]
        return extra + urls

    def batch_promos_view(self, request, seller_id, batch_id):
        try:
            seller = Seller.objects.get(pk=seller_id)
            batch = SellerBatch.objects.get(pk=batch_id, seller=seller)
        except (Seller.DoesNotExist, SellerBatch.DoesNotExist):
            return HttpResponse('Topilmadi', status=404)

        qrcodes = batch.get_qrcodes()
        rows = []
        for qr in qrcodes:
            if qr.is_scanned and qr.scanned_by:
                sb = qr.scanned_by
                sb_name = sb.first_name or sb.username or str(sb.telegram_id)
                sb_url = reverse('admin:core_telegramuser_change', args=[sb.pk])
                scanned_by_html = format_html('<a href="{}">{}</a>', sb_url, sb_name)
            elif qr.is_scanned:
                scanned_by_html = format_html('<span style="color:#16a34a;">✅ Ha</span>')
            else:
                scanned_by_html = format_html('<span style="color:#9ca3af;">—</span>')

            rows.append({
                'seq': qr.sequence_number,
                'serial': qr.serial_number,
                'is_scanned': qr.is_scanned,
                'scanned_by_html': scanned_by_html,
                'scanned_at': qr.scanned_at.strftime('%d.%m.%Y %H:%M') if qr.scanned_at else '—',
            })

        context = {
            **self.admin_site.each_context(request),
            'seller': seller,
            'batch': batch,
            'rows': rows,
            'total': len(rows),
            'activated': batch.activated_count(),
            'activation_pct': batch.activation_percent(),
            'title': f"{seller.name} — Partiya #{batch_id} promolari",
            'opts': Seller._meta,
        }
        return TemplateResponse(request, 'admin/core/seller/batch_promos.html', context)
