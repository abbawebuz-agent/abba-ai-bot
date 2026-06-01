"""
URL configuration for mona project.
"""
from django.contrib import admin
from django.contrib.auth import logout
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.template.response import TemplateResponse
from django.shortcuts import redirect, get_object_or_404
from django.utils import timezone
from django.db.models import Count, Sum, Q
from django.core.paginator import Paginator
from django.http import HttpResponse, FileResponse
from datetime import date, timedelta, datetime
from urllib.parse import urlencode
from django.utils.translation import gettext as _, get_language
import os
from core.dashboard_stats import (
    DASHBOARD_REGION_ORDER,
    build_promo_table_rows,
    compute_general_stats,
    compute_dashboard_charts,
    compute_intelligence_stats,
    get_user_crm_details,
    compute_store_analytics,
)
from core.dashboard_exports import generate_full_dashboard_excel, generate_module_excel, generate_regional_excel
from core.models import UzRegion, TelegramUser, QRCode, Gift, GiftRedemption, UzDistrict


def _is_call_center_user(user) -> bool:
    """Call-center пользователь: username callcenter, или имеет call_center права, и не суперюзер."""
    if not user.is_authenticated or user.is_superuser:
        return False
    if getattr(user, 'username', '') == 'callcenter':
        return True
    return (
        user.has_perm('core.change_status_call_center')
        or user.has_perm('core.change_user_type_call_center')
    )


def _parse_date(s):
    """Парсит строку YYYY-MM-DD в date или None."""
    if not s:
        return None
    try:
        return date.fromisoformat(s.strip())
    except (ValueError, TypeError):
        return None


def _dashboard_query_suffix(date_from, date_to, region_code='', tab=''):
    """Фрагмент query string (без ?): tab, даты, опционально region."""
    parts = []
    if tab:
        parts.append(f'tab={tab}')
    if date_from:
        parts.append(f'date_from={date_from.isoformat()}')
    if date_to:
        parts.append(f'date_to={date_to.isoformat()}')
    if region_code:
        parts.append(f'region={region_code}')
    return '&'.join(parts)


def _local_today():
    return timezone.localdate()


def _resolve_dashboard_dates(request):
    """
    Приоритет: preset → ручные date_from/date_to в GET → по умолчанию текущий месяц.
    Возвращает (date_from, date_to, is_explicit).
    is_explicit = True, если пользователь явно выбрал период (через пресет или даты).
    """
    preset = (request.GET.get('preset') or '').strip()
    df_key = 'date_from' in request.GET
    dt_key = 'date_to' in request.GET
    is_explicit = bool(preset or df_key or dt_key)

    if preset == 'all':
        return None, None, True
    if preset == 'current_month':
        today = _local_today()
        return today.replace(day=1), today, True
    if preset == 'last_7_days':
        today = _local_today()
        return today - timedelta(days=6), today, True
    if preset == 'last_month':
        today = _local_today()
        first_this = today.replace(day=1)
        end_prev = first_this - timedelta(days=1)
        return end_prev.replace(day=1), end_prev, True

    if df_key or dt_key:
        return _parse_date(request.GET.get('date_from')), _parse_date(
            request.GET.get('date_to')
        ), True

    today = _local_today()
    return today.replace(day=1), today, False


def _detect_active_date_preset(date_from, date_to) -> str:
    """Какая из быстрых кнопок соответствует текущему диапазону (или custom)."""
    if date_from is None and date_to is None:
        return 'all'
    today = _local_today()
    first_cm = today.replace(day=1)
    if date_from == first_cm and date_to == today:
        return 'current_month'
    if date_from == today - timedelta(days=6) and date_to == today:
        return 'last_7_days'
    first_this = today.replace(day=1)
    end_prev = first_this - timedelta(days=1)
    first_prev = end_prev.replace(day=1)
    if date_from == first_prev and date_to == end_prev:
        return 'last_month'
    return 'custom'


def _promocodes_back_query(request):
    """Query string для возврата к списку промокодов (без qr)."""
    data = {k: v for k, v in request.GET.items() if k != 'qr' and v != ''}
    data['tab'] = 'promocodes'
    return urlencode(data)


def _promo_qr_winner_context(qr):
    """Данные победителя по отсканированному промокоду (для лототрона)."""
    u = qr.scanned_by
    if not u:
        return {
            'has_user': False,
            'username': '',
            'full_name': '',
            'phone': '',
            'address': '',
        }
    full_name = ' '.join(
        part for part in [u.first_name or '', u.last_name or ''] if part
    ).strip()
    addr_parts = []
    if u.region_id:
        addr_parts.append(u.region.name_uz or '')
    if u.district_id:
        addr_parts.append(u.district.name_uz or '')
    if u.latitude is not None and u.longitude is not None:
        addr_parts.append(f'{u.latitude:.5f}, {u.longitude:.5f}')
    address = ', '.join(p for p in addr_parts if p) or '—'
    return {
        'has_user': True,
        'username': u.username or '',
        'full_name': full_name or '—',
        'phone': u.phone_number or '—',
        'address': address,
    }


def dashboard_export_view(request):
    """
    Генерирует Excel-файл на основе текущих фильтров и выбранного модуля (Summary vs Parallel Details).
    Force localized to UZ.
    """
    if _is_call_center_user(request.user):
        return redirect('admin:index')
    date_from, date_to, is_explicit = _resolve_dashboard_dates(request)
    tab = (request.GET.get('tab') or 'general').strip().lower()
    module = (request.GET.get('module') or 'general_summary').strip().lower()
    
    # Common filters
    drill_region_code = (request.GET.get('region') or '').strip()
    drill_region = UzRegion.objects.filter(code=drill_region_code).first() if drill_region_code else None
    search_q = (request.GET.get('q') or '').strip()
    status_filter = (request.GET.get('status') or '').strip()
    user_type_filter = (request.GET.get('user_type') or '').strip()
    
    # 1. Handle Module Selection
    filename_prefix = "Dashboard_Export"
    output = None

    if module == 'general_summary':
        # Legacy summary sheet + Trends + Regional
        g_stats = compute_general_stats(date_from, date_to)
        stats = {
            'general_stats': g_stats,
            'charts': compute_dashboard_charts(date_from, date_to, drill_region=drill_region),
            'intelligence_stats': compute_intelligence_stats(date_from, date_to),
            'promo_rows': build_promo_table_rows('seller' if tab == 'stores' else 'electrician', date_from, date_to, drill_region, global_stats=g_stats),
            'tab': tab,
            'drill_region_name': drill_region.name_uz if drill_region else None,
        }
        output = generate_full_dashboard_excel(stats)
        filename_prefix = f"Summary_{tab}"

    elif module == 'users_list':
        # Detailed user list with CRM filters
        u_qs = TelegramUser.objects.all().select_related('region', 'district').order_by('-created_at')
        if search_q:
            u_qs = u_qs.filter(Q(username__icontains=search_q) | Q(first_name__icontains=search_q) | Q(last_name__icontains=search_q) | Q(phone_number__icontains=search_q))
        if date_from and (is_explicit or not search_q):
            u_qs = u_qs.filter(created_at__date__gte=date_from)
        if date_to and (is_explicit or not search_q):
            u_qs = u_qs.filter(created_at__date__lte=date_to)
        if user_type_filter:
            u_qs = u_qs.filter(user_type=user_type_filter)
        if drill_region:
            u_qs = u_qs.filter(region=drill_region)
            
        headers = [
            ('id', 'col_id'), ('telegram_id', 'col_tg_id'), ('first_name', 'col_first_name'),
            ('last_name', 'col_last_name'), ('username', 'col_username'), ('phone_number', 'col_phone'),
            ('user_type', 'col_type'), ('region', 'col_region'), ('district', 'col_district'),
            ('points', 'col_points'), ('created_at', 'col_joined_at')
        ]
        output = generate_module_excel('users_list', u_qs, headers)
        filename_prefix = "Users_Detailed_List"

    elif module == 'redemptions_list':
        # Detailed redemption log
        r_qs = GiftRedemption.objects.all().select_related('user', 'gift').order_by('-requested_at')
        if search_q:
            r_qs = r_qs.filter(Q(user__username__icontains=search_q)|Q(user__first_name__icontains=search_q)|Q(gift__name_uz_latin__icontains=search_q)|Q(gift__name_ru__icontains=search_q))
        if date_from and (is_explicit or not search_q):
            r_qs = r_qs.filter(requested_at__date__gte=date_from)
        if date_to and (is_explicit or not search_q):
            r_qs = r_qs.filter(requested_at__date__lte=date_to)
        if status_filter:
            r_qs = r_qs.filter(status=status_filter)
        if user_type_filter:
            r_qs = r_qs.filter(user__user_type=user_type_filter)
        if drill_region:
            r_qs = r_qs.filter(user__region=drill_region)
            
        headers = [
            ('id', 'col_id'), (lambda x: f"{x.user.first_name} (@{x.user.username})", 'col_user'),
            (lambda x: x.gift.name_uz_latin, 'col_gift_name'), ('status', 'col_status'),
            (lambda x: x.gift.points_cost, 'col_points_cost'), ('requested_at', 'col_requested_at'),
            ('admin_notes', 'col_admin_notes'), ('confirmed_at', 'col_confirmed_at')
        ]
        output = generate_module_excel('redemptions_list', r_qs, headers)
        filename_prefix = "Redemptions_Log"

    elif module == 'activations_list':
        # Activation Feed / Scans Feed
        pc_qs = QRCode.objects.filter(is_deleted=False, is_scanned=True).select_related('scanned_by', 'scanned_by__region').order_by('-scanned_at')
        if search_q:
            pc_qs = pc_qs.filter(Q(code__icontains=search_q)|Q(serial_number__icontains=search_q)|Q(scanned_by__username__icontains=search_q)|Q(scanned_by__first_name__icontains=search_q))
        if date_from and (is_explicit or not search_q):
            pc_qs = pc_qs.filter(scanned_at__date__gte=date_from)
        if date_to and (is_explicit or not search_q):
            pc_qs = pc_qs.filter(scanned_at__date__lte=date_to)
        if drill_region:
            pc_qs = pc_qs.filter(scanned_by__region=drill_region)
            
        headers = [
            ('serial_number', 'col_serial'), ('code', 'col_promo_code'), ('points', 'col_points_val'),
            (lambda x: x.store.name if x.store_id else '-', 'col_store'), ('scanned_at', 'col_scanned_at'),
            (lambda x: f"{x.scanned_by.first_name} (@{x.scanned_by.username})", 'col_scanned_by'),
            (lambda x: x.scanned_by.phone_number, 'col_phone'),
            (lambda x: x.scanned_by.region.name_uz if x.scanned_by.region else "N/A", 'col_region')
        ]
        output = generate_module_excel('activations_list', pc_qs, headers)
        filename_prefix = "QR_Activations_Log"

    elif module == 'gifts_list':
        g_qs = Gift.objects.all().order_by('order')
        headers = [
            ('id', 'col_id'), ('name_uz_latin', 'col_gift_name'), ('points_cost', 'col_points_cost'),
            ('user_type', 'col_type'), ('is_active', 'col_status')
        ]
        output = generate_module_excel('gifts_list', g_qs, headers)
        filename_prefix = "Gifts_Inventory"

    elif module == 'regional_list':
        # Specific regional breakdown table
        g_stats = compute_general_stats(date_from, date_to)
        stats = {
            'promo_rows': build_promo_table_rows('seller' if tab == 'stores' else 'electrician', date_from, date_to, drill_region, global_stats=g_stats),
            'tab': tab,
            'drill_region_name': drill_region.name_uz if drill_region else None,
        }
        output = generate_regional_excel(stats)
        filename_prefix = f"Regional_Breakdown_{tab}"

    # 3. Build Response
    filename = f"{filename_prefix}_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx"
    response = HttpResponse(
        output.read(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response


def dashboard_view(request):
    """Дашборд: вкладки Umumiy / do'konlar / elektriklar / promokodlar и фильтр по датам."""
    is_cc = _is_call_center_user(request.user)
    date_from, date_to, is_explicit = _resolve_dashboard_dates(request)
    tab = (request.GET.get('tab') or 'general').strip().lower()
    if is_cc:
        tab = 'redemptions'
    if tab not in ('general', 'stores', 'electricians', 'promocodes', 'users', 'gifts', 'redemptions'):
        tab = 'general'

    drill_region_code = (request.GET.get('region') or '').strip()
    selected_district = (request.GET.get('district') or '').strip()
    drill_region = (
        UzRegion.objects.filter(code=drill_region_code).first()
        if drill_region_code
        else None
    )
    if drill_region_code and drill_region is None and drill_region_code != 'undefined':
        drill_region_code = ''

    if tab in ('general', 'promocodes'):
        drill_region = None
        drill_region_code = ''
        selected_district = ''

    lang_code = get_language()[:2]
    user_language = 'ru' if lang_code == 'ru' else 'uz_latin'

    if date_from is None and date_to is None:
        if lang_code == 'uz':
            period_label = "Butun davr"
        elif lang_code == 'ru':
            period_label = "Весь период"
        else:
            period_label = _('Butun davr')
    elif date_from is not None and date_to is not None:
        period_label = f'{date_from.strftime("%d/%m/%Y")} — {date_to.strftime("%d/%m/%Y")}'
    elif date_from is not None:
        if lang_code == 'uz':
            period_label = f'{date_from.strftime("%d/%m/%Y")} dan'
        elif lang_code == 'ru':
            period_label = f'С {date_from.strftime("%d/%m/%Y")}'
        else:
            period_label = _('{date_from} dan').format(date_from=date_from.strftime("%d/%m/%Y"))
    else:
        if lang_code == 'uz':
            period_label = f'{date_to.strftime("%d/%m/%Y")} gacha'
        elif lang_code == 'ru':
            period_label = f'До {date_to.strftime("%d/%m/%Y")}'
        else:
            period_label = _('{date_to} gacha').format(date_to=date_to.strftime("%d/%m/%Y"))

    active_date_preset = _detect_active_date_preset(date_from, date_to)

    general_stats = None
    charts = None
    promo_rows = []
    selected_users = []
    selected_scope_label = ''
    promo_codes_page = None
    # Tasdiqlanmagan sotuvchilar soni
    pending_sellers_count = TelegramUser.objects.filter(user_type='sotuvchi', seller_approved=False).count()
    promo_qr_detail = None
    promo_winner = None
    promocodes_back_query = ''
    promocodes_search_q = ''
    lang_code = get_language()[:2]
    filter_labels = {
        'day7': '7D',
        'month1': '1M',
        'prev': 'Prev. Month',
        'all': _('Lifetime')
    }
    if lang_code == 'ru':
        filter_labels.update({'day7': '7Дн', 'month1': '1М', 'prev': 'Прош. месяц', 'all': 'Все время'})
    elif lang_code == 'uz':
        filter_labels.update({'day7': '7 Kun', 'month1': '1 Oy', 'prev': "O'tgan oy", 'all': "Hamma vaqt"})

    intelligence_stats = None
    
    # New Contexts
    crm_users_page = None
    gifts_page = None
    redemptions_page = None
    redemption_stats = {}
    regions_list = []
    store_rows = []
    store_totals = {}
    crm_search_q = (request.GET.get('q') or '').strip()
    crm_ut = request.GET.get('user_type', '')
    crm_reg = request.GET.get('region', '')
    # Sorting & Filtering Defaults
    crm_sort = request.GET.get('ordering', '')
    r_sort = ''
    p_sort = ''
    
    if tab == 'users':
        if not crm_sort: crm_sort = '-created_at'
    elif tab == 'redemptions':
        r_sort = crm_sort or '-requested_at'
    elif tab == 'promocodes':
        p_sort = crm_sort or '-scanned_at'
    elif tab in ('stores', 'electricians'):
        if not crm_sort: crm_sort = '-points'
    crm_status = request.GET.get('status', '')
    selected_activity = (request.GET.get('activity') or '').strip().lower()
    if selected_activity not in ('active', 'inactive'):
        selected_activity = ''

    if tab == 'general':
        general_stats = compute_general_stats(date_from, date_to)
        charts = compute_dashboard_charts(date_from, date_to, drill_region=drill_region)
        intelligence_stats = compute_intelligence_stats(date_from, date_to)
    elif tab == 'users':
        general_stats = compute_general_stats(date_from, date_to)
        charts = compute_dashboard_charts(date_from, date_to, drill_region=drill_region)
        intelligence_stats = compute_intelligence_stats(date_from, date_to)
        regions_list = [{'code': r.code, 'name': (r.name_ru if get_language()[:2] == 'ru' and r.name_ru else r.name_uz)} for r in UzRegion.objects.all()]
        regions_list.append({'code': 'undefined', 'name': _("Noma'lum")})
        u_qs = TelegramUser.objects.all().select_related('region', 'district').order_by(crm_sort)
        if crm_search_q:
            u_qs = u_qs.filter(Q(username__icontains=crm_search_q)|Q(first_name__icontains=crm_search_q)|Q(last_name__icontains=crm_search_q)|Q(phone_number__icontains=crm_search_q))
        if date_from and (is_explicit or not crm_search_q):
            u_qs = u_qs.filter(created_at__date__gte=date_from)
        if date_to and (is_explicit or not crm_search_q):
            u_qs = u_qs.filter(created_at__date__lte=date_to)
        if crm_ut:
            u_qs = u_qs.filter(user_type=crm_ut)
        if crm_reg:
            if crm_reg == 'undefined':
                u_qs = u_qs.filter(region__isnull=True)
            else:
                u_qs = u_qs.filter(region__code=crm_reg)
        if drill_region:
            u_qs = u_qs.filter(region=drill_region)
        try:
            page_num = max(1, int(request.GET.get('page') or 1))
        except ValueError:
            page_num = 1
        crm_users_page = Paginator(u_qs, 20).get_page(page_num)
    elif tab == 'gifts':
        general_stats = compute_general_stats(date_from, date_to)
        charts = compute_dashboard_charts(date_from, date_to, drill_region=drill_region)
        intelligence_stats = compute_intelligence_stats(date_from, date_to)
        g_qs = Gift.objects.filter(is_active=True).order_by('-points_cost')
        if crm_search_q:
            g_qs = g_qs.filter(Q(name_uz_latin__icontains=crm_search_q)|Q(name_ru__icontains=crm_search_q))
        try:
            page_num = max(1, int(request.GET.get('page') or 1))
        except ValueError:
            page_num = 1
        gifts_page = Paginator(g_qs, 20).get_page(page_num)
    elif tab == 'redemptions':
        general_stats = compute_general_stats(date_from, date_to)
        charts = compute_dashboard_charts(date_from, date_to, drill_region=drill_region)
        intelligence_stats = compute_intelligence_stats(date_from, date_to)
        r_qs = GiftRedemption.objects.all().select_related('user', 'gift').order_by(r_sort)
        if crm_search_q:
            r_qs = r_qs.filter(Q(user__username__icontains=crm_search_q)|Q(user__first_name__icontains=crm_search_q)|Q(gift__name_uz_latin__icontains=crm_search_q)|Q(gift__name_ru__icontains=crm_search_q))
        if date_from and (is_explicit or not crm_search_q):
            r_qs = r_qs.filter(requested_at__date__gte=date_from)
        if date_to and (is_explicit or not crm_search_q):
            r_qs = r_qs.filter(requested_at__date__lte=date_to)
        if crm_status:
            r_qs = r_qs.filter(status=crm_status)
        if crm_ut:
            r_qs = r_qs.filter(user__user_type=crm_ut)
        if drill_region:
            r_qs = r_qs.filter(user__region=drill_region)
        
        # Stats for Redemptions Banner
        redemption_stats = {
            'total': r_qs.count(),
            'pending': r_qs.filter(status='pending').count(),
            'approved': r_qs.filter(status='approved').count(),
            'sent': r_qs.filter(status='sent').count(),
            'issued': r_qs.filter(status='completed').count(),
            'rejected': r_qs.filter(status='rejected').count(),
            'cancelled': r_qs.filter(status='cancelled_by_user').count(),
            'not_received': r_qs.filter(status='not_received').count(),
            'spent_points': r_qs.filter(status='completed').aggregate(s=Sum('gift__points_cost'))['s'] or 0
        }
        
        try:
            page_num = max(1, int(request.GET.get('page') or 1))
        except ValueError:
            page_num = 1
        redemptions_page = Paginator(r_qs, 20).get_page(page_num)
    elif tab == 'stores':
        general_stats = compute_general_stats(date_from, date_to)
        charts = compute_dashboard_charts(date_from, date_to, drill_region=drill_region)
        intelligence_stats = compute_intelligence_stats(date_from, date_to)
        promo_rows = build_promo_table_rows('seller', date_from, date_to, drill_region, global_stats=general_stats)
        store_rows, store_totals = compute_store_analytics(date_from, date_to)
        if crm_sort:
            reverse = crm_sort.startswith('-')
            field = crm_sort.lstrip('-')
            if field in ['users', 'cards', 'points', 'spent', 'name']:
                promo_rows.sort(key=lambda x: (x.get('is_total', False), x.get(field, 0) if field != 'name' else x.get(field, '')), reverse=reverse)
            if field in ['total_qr', 'scanned_life', 'scanned_period', 'act_rate_life', 'batch_count', 'name']:
                store_rows.sort(key=lambda x: x.get(field, 0) if field != 'name' else x.get(field, ''), reverse=reverse)
    elif tab == 'electricians':
        general_stats = compute_general_stats(date_from, date_to)
        charts = compute_dashboard_charts(date_from, date_to, drill_region=drill_region)
        intelligence_stats = compute_intelligence_stats(date_from, date_to)
        promo_rows = build_promo_table_rows('electrician', date_from, date_to, drill_region, global_stats=general_stats)
        if crm_sort:
            reverse = crm_sort.startswith('-')
            field = crm_sort.lstrip('-')
            if field in ['users', 'cards', 'points', 'spent', 'name']:
                promo_rows.sort(key=lambda x: (x.get('is_total', False), x.get(field, 0) if field != 'name' else x.get(field, '')), reverse=reverse)
    elif tab == 'promocodes':
        general_stats = compute_general_stats(date_from, date_to)
        charts = compute_dashboard_charts(date_from, date_to, drill_region=drill_region)
        intelligence_stats = compute_intelligence_stats(date_from, date_to)
        promocodes_search_q = (request.GET.get('q') or '').strip()
        promocodes_back_query = _promocodes_back_query(request)
        qr_raw = (request.GET.get('qr') or '').strip()
        if qr_raw:
            try:
                promo_qr_detail = QRCode.objects.select_related(
                    'scanned_by',
                    'scanned_by__region',
                    'scanned_by__district',
                ).get(
                    pk=int(qr_raw),
                    is_deleted=False,
                    is_scanned=True,
                )
                promo_winner = _promo_qr_winner_context(promo_qr_detail)
            except (ValueError, QRCode.DoesNotExist):
                promo_qr_detail = None
                promo_winner = None
        pc_qs = (
            QRCode.objects.filter(is_deleted=False, is_scanned=True)
            .select_related(
                'scanned_by',
                'scanned_by__region',
                'scanned_by__district',
            )
            .order_by(p_sort if p_sort else '-scanned_at', '-id')
        )
        if date_from and (is_explicit or not promocodes_search_q):
            pc_qs = pc_qs.filter(scanned_at__date__gte=date_from)
        if date_to and (is_explicit or not promocodes_search_q):
            pc_qs = pc_qs.filter(scanned_at__date__lte=date_to)
        if drill_region:
            pc_qs = pc_qs.filter(scanned_by__region=drill_region)
        if promocodes_search_q:
            sq = promocodes_search_q
            pc_qs = pc_qs.filter(
                Q(code__icontains=sq)
                | Q(serial_number__icontains=sq)
                | Q(hash_code__icontains=sq)
                | Q(scanned_by__username__icontains=sq)
                | Q(scanned_by__first_name__icontains=sq)
                | Q(scanned_by__last_name__icontains=sq)
                | Q(scanned_by__phone_number__icontains=sq)
            )
        try:
            page_num = max(1, int(request.GET.get('page') or 1))
        except ValueError:
            page_num = 1
        promo_codes_page = Paginator(pc_qs, 15).get_page(page_num)

    if tab in ('stores', 'electricians') and ((drill_region and selected_district) or drill_region_code == 'undefined'):
        user_type = 'seller' if tab == 'stores' else 'electrician'
        
        if drill_region_code == 'undefined':
            listed_ids = list(UzRegion.objects.filter(code__in=DASHBOARD_REGION_ORDER).values_list('pk', flat=True))
            user_qs = TelegramUser.objects.filter(
                Q(region_id__isnull=True) | ~Q(region_id__in=listed_ids),
                user_type=user_type,
            ).select_related('district', 'region')
            selected_scope_label = _("Noma'lum")
        else:
            user_qs = TelegramUser.objects.filter(
                user_type=user_type,
                region_id=drill_region.pk,
            ).select_related('district')

            if selected_district == 'none':
                user_qs = user_qs.filter(district__isnull=True)
                selected_scope_label = _('Tuman tanlanmagan')
            elif selected_district.isdigit():
                did = int(selected_district)
                user_qs = user_qs.filter(district_id=did)
                d_obj = drill_region.districts.filter(pk=did).first()
                selected_scope_label = d_obj.name_uz if d_obj else f'Tuman #{did}'
            else:
                user_qs = user_qs.none()

        qr_filter = Q(scanned_qrcodes__is_scanned=True)
        if date_from is not None:
            qr_filter &= Q(scanned_qrcodes__scanned_at__date__gte=date_from)
        if date_to is not None:
            qr_filter &= Q(scanned_qrcodes__scanned_at__date__lte=date_to)

        user_qs = user_qs.annotate(
            scanned_cards=Count('scanned_qrcodes', filter=qr_filter),
            scanned_points=Sum('scanned_qrcodes__points', filter=qr_filter),
        )

        if selected_activity:
            # Регистрация завершена: имя, телефон, тип, согласие, координаты;
            # для seller дополнительно требуется SmartUP ID (см. bot.is_registration_complete).
            registered_q = (
                Q(first_name__isnull=False) & ~Q(first_name='')
                & Q(phone_number__isnull=False) & ~Q(phone_number='')
                & Q(user_type__isnull=False) & ~Q(user_type='')
                & Q(privacy_accepted=True)
                & Q(latitude__isnull=False)
                & Q(longitude__isnull=False)
            )
            if selected_activity == 'active':
                # Заполнил все данные И отсканировал хотя бы один промокод.
                user_qs = user_qs.filter(registered_q).filter(scanned_cards__gt=0)
            else:  # inactive — не завершил регистрацию.
                user_qs = user_qs.exclude(registered_q)

        if crm_sort:
            user_qs = user_qs.order_by(crm_sort)
        else:
            user_qs = user_qs.order_by('-scanned_points', '-scanned_cards', '-created_at')

        for u in user_qs[:300]:
            full_name = ' '.join(
                part for part in [u.first_name or '', u.last_name or ''] if part
            ).strip()
            selected_users.append(
                {
                    'id': u.pk,
                    'name': full_name or (f'@{u.username}' if u.username else f'ID {u.telegram_id}'),
                    'username': u.username or '',
                    'phone': u.phone_number or '—',
                    'region': u.region.name_uz if u.region else '—',
                    'district': u.district.name_uz if u.district else '—',
                    'cards': u.scanned_cards or 0,
                    'points': u.scanned_points or 0,
                }
            )

    dq_base = _dashboard_query_suffix(date_from, date_to, '', tab)
    dq_back_viloyat = dq_base

    context = {
        **admin.site.each_context(request),
        'title': 'Dashboard',
        'period_label': period_label,
        'date_from': date_from.isoformat() if date_from else '',
        'date_to': date_to.isoformat() if date_to else '',
        'tab': tab,
        'active_date_preset': active_date_preset,
        'general_stats': general_stats,
        'charts': charts,
        'promo_rows': promo_rows,
        'drill_region': drill_region,
        'drill_region_code': drill_region_code,
        'drill_region_name': (drill_region.name_ru if get_language()[:2] == 'ru' and drill_region.name_ru else drill_region.name_uz) if drill_region else '',
        'dashboard_date_query': dq_base,
        'dashboard_back_viloyat_query': dq_back_viloyat,
        'selected_district': selected_district,
        'selected_activity': selected_activity,
        'selected_users': selected_users,
        'selected_scope_label': selected_scope_label,
        'promo_codes_page': promo_codes_page,
        'promo_qr_detail': promo_qr_detail,
        'promo_winner': promo_winner,
        'promocodes_search_q': promocodes_search_q,
        'promocodes_back_query': promocodes_back_query,
        'intelligence_stats': intelligence_stats,
        'crm_users_page': crm_users_page,
        'gifts_page': gifts_page,
        'redemptions_page': redemptions_page,
        'redemption_stats': redemption_stats,
        'regions_list': regions_list,
        'crm_search_q': crm_search_q,
        'user_language': user_language,
        'crm_ut': crm_ut,
        'crm_reg': crm_reg,
        'crm_sort': crm_sort or r_sort or p_sort or '-created_at',
        'crm_status': crm_status,
        'redemption_status_choices': GiftRedemption.STATUS_CHOICES,
        'filter_labels': filter_labels,
        'is_cc': is_cc,
        'store_rows': store_rows,
        'store_totals': store_totals,
        'pending_sellers_count': pending_sellers_count,
    }

    # For AJAX infinite-scroll requests, return only the rows partial
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return TemplateResponse(request, 'admin/dashboard_rows.html', context)

    return TemplateResponse(request, 'admin/dashboard.html', context)


def user_detail_view(request, user_id):
    """Детальная CRM-страница пользователя: статистика, история сканов и наград."""
    user = get_object_or_404(TelegramUser, pk=user_id)
    crm = get_user_crm_details(user_id)

    context = {
        **admin.site.each_context(request),
        'title': f'CRM: {user.first_name or user.username}',
        'member': user,
        'crm': crm,
        'is_cc': _is_call_center_user(request.user),
    }
    return TemplateResponse(request, 'admin/user_detail.html', context)


def admin_logout_view(request):
    """Кастомный обработчик logout для админки, поддерживающий GET-запросы."""
    logout(request)
    return redirect(settings.LOGIN_URL)


from core.bot_webhook import telegram_webhook_view



def root_redirect(request):
    """Bosh sahifa / → /admin/ ga redirect (BUG-006)."""
    return redirect('/admin/')


def health_check(request):
    """Railway/Docker healthcheck endpoint — no auth, always 200."""
    return HttpResponse('OK', content_type='text/plain', status=200)


def admin_send_dev_update_view(request):
    """JIP Development guruhiga dev update xabarini yuboradi.
    GET: msg=<text>, chat_id=<optional>
    """
    import json, urllib.request, urllib.parse, urllib.error
    from django.conf import settings
    from django.contrib import messages as dj_messages

    if not request.user.is_superuser:
        from django.http import HttpResponseForbidden
        return HttpResponseForbidden("Faqat superuser uchun")

    token = settings.TELEGRAM_BOT_TOKEN
    if not token:
        dj_messages.error(request, "TELEGRAM_BOT_TOKEN topilmadi")
        return redirect('admin:index')

    msg = request.GET.get('msg', '').strip()
    if not msg:
        dj_messages.error(request, "?msg= parametri kerak")
        return redirect('admin:index')

    def tg_call(method, payload=None, is_get=False, params=None):
        url = f"https://api.telegram.org/bot{token}/{method}"
        if is_get and params:
            url += "?" + urllib.parse.urlencode(params)
        try:
            if is_get:
                req = urllib.request.Request(url)
            else:
                data = json.dumps(payload or {}).encode()
                req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=10) as r:
                return json.loads(r.read())
        except urllib.error.HTTPError as e:
            try:
                return json.loads(e.read())
            except Exception:
                return {"ok": False, "description": str(e)}
        except Exception as e:
            return {"ok": False, "description": str(e)}

    # If chat_id provided directly, skip discovery
    chat_id = request.GET.get('chat_id', '').strip()
    group_name = chat_id or "guruh"

    if not chat_id:
        # Webhook aktiv bo'lganda getUpdates ishlamaydi → vaqtincha o'chiramiz
        wh_info = tg_call("getWebhookInfo", is_get=True)
        webhook_url = (wh_info.get("result") or {}).get("url", "")

        tg_call("deleteWebhook", {"drop_pending_updates": False})

        upd_data = tg_call("getUpdates", is_get=True, params={"limit": 50, "offset": -50})

        # Darhol webhookni qayta qo'yamiz
        if webhook_url:
            tg_call("setWebhook", {"url": webhook_url, "drop_pending_updates": False})

        for upd in reversed((upd_data or {}).get("result", [])):
            raw_msg = upd.get("message") or {}
            mc = (upd.get("my_chat_member") or {})
            chat = raw_msg.get("chat") or mc.get("chat") or {}
            if isinstance(chat, dict) and chat.get("type") in ("group", "supergroup"):
                chat_id = str(chat["id"])
                group_name = chat.get("title", chat_id)
                break

        if not chat_id:
            dj_messages.error(request,
                "Guruh topilmadi. URL ga &chat_id=GROUP_ID parametrini qo'shing")
            return redirect('admin:index')

    send_data = tg_call("sendMessage", {"chat_id": int(chat_id), "text": msg, "parse_mode": "HTML"})

    if send_data.get("ok"):
        dj_messages.success(request, f"✅ '{group_name}' ({chat_id}) guruhiga yuborildi")
    else:
        dj_messages.error(request, f"❌ Telegram: {send_data.get('description', send_data)}")
    return redirect('admin:index')


def admin_backup_test_view(request):
    """Test BACKUP_CHANNEL_ID + bot ulanish (diagnostika)."""
    import io
    from django.contrib import messages
    from django.core.management import call_command

    if not request.user.is_superuser:
        from django.http import HttpResponseForbidden
        return HttpResponseForbidden("Faqat superuser uchun")

    out = io.StringIO()
    err = io.StringIO()
    try:
        call_command('test_backup_channel', stdout=out, stderr=err)
        log = out.getvalue() or err.getvalue()
        messages.success(request, f"🧪 Test natijasi:\n\n{log}")
    except Exception as exc:
        log = (out.getvalue() or '') + '\n' + (err.getvalue() or '')
        messages.error(request, f"❌ Test xato:\n\n{exc}\n\nLog:\n{log}")
    return redirect('admin:index')


def admin_backup_now_view(request):
    """Admin paneldagi "Backup ni Telegramga yuklash" tugma.

    SYNC: pg_dump → Telegram channel. Xato bo'lsa real message ko'rsatadi.
    """
    import io, logging, traceback
    from django.contrib import messages
    from django.conf import settings
    from django.core.management import call_command

    logger = logging.getLogger(__name__)

    if not request.user.is_superuser:
        from django.http import HttpResponseForbidden
        return HttpResponseForbidden("Faqat superuser uchun")

    chat_id = getattr(settings, 'BACKUP_CHANNEL_ID', '') or os.environ.get('BACKUP_CHANNEL_ID', '')
    if not chat_id:
        messages.error(
            request,
            "❌ BACKUP_CHANNEL_ID sozlanmagan. Railway Variables'da qo'shing."
        )
        return redirect('admin:index')

    from core.models import log_event, ActivityLog as _AL
    out = io.StringIO()
    err = io.StringIO()
    try:
        call_command('backup_db', stdout=out, stderr=err)
        log = out.getvalue() or err.getvalue()
        logger.info("admin_backup_now OK:\n%s", log)
        # Show last 3 lines as success message
        last_lines = '\n'.join(log.strip().splitlines()[-3:])
        messages.success(
            request,
            f"✅ Backup muvaffaqiyatli! Telegram kanalingizni tekshiring.\n\n{last_lines}"
        )
        log_event(
            action_type=_AL.ACTION_BACKUP, user=request.user,
            description=f"Manual backup → Telegram channel ({chat_id})",
            request=request,
            channel_id=str(chat_id),
            log_tail=last_lines[:500],
        )
    except Exception as exc:
        tb = traceback.format_exc()
        logger.error("admin_backup_now FAILED:\n%s\n\nSTDOUT:\n%s\nSTDERR:\n%s",
                     tb, out.getvalue(), err.getvalue())
        # Show error to admin
        err_msg = str(exc)[:500]
        stdout_msg = (out.getvalue() or '')[-500:]
        stderr_msg = (err.getvalue() or '')[-500:]
        full_msg = (
            f"❌ Backup xato:\n\n"
            f"{type(exc).__name__}: {err_msg}\n\n"
        )
        if stdout_msg.strip():
            full_msg += f"STDOUT:\n{stdout_msg}\n\n"
        if stderr_msg.strip():
            full_msg += f"STDERR:\n{stderr_msg}"
        messages.error(request, full_msg)
        try:
            from core.models import log_event, ActivityLog as _AL
            log_event(
                action_type=_AL.ACTION_ERROR, user=request.user,
                description=f"Backup xato: {type(exc).__name__}: {str(exc)[:200]}",
                request=request,
            )
        except Exception:
            pass
    return redirect('admin:index')


def jip_admin_spa_view(request, **kwargs):
    """JIP Admin SPA — serves the React admin panel with real DB stats injected."""
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('/admin/login/?next=/jip-admin/')
    import logging, traceback as _tb
    _log = logging.getLogger(__name__)
    try:
        from core.models import QRCodeBatch, SellerPointsTransaction, ActivityLog
        stats = {
            'users_total':    TelegramUser.objects.count(),
            'users_santenik': TelegramUser.objects.filter(user_type='santenik').count(),
            'users_sotuvchi': TelegramUser.objects.filter(user_type='sotuvchi').count(),
            'batches_total':  QRCodeBatch.objects.count(),
            'batches_active': QRCodeBatch.objects.filter(status='active').count(),
            'qr_total':       QRCode.objects.count(),
            'qr_scanned':     QRCode.objects.filter(is_used=True).count(),
            'gifts_pending':  GiftRedemption.objects.filter(status='pending').count(),
            'txns_total':     SellerPointsTransaction.objects.count(),
            'audit_total':    ActivityLog.objects.count(),
        }
    except Exception as _e:
        _log.error('jip_admin stats error: %s\n%s', _e, _tb.format_exc())
        stats = {'_error': str(_e)}
    return TemplateResponse(request, 'jip_admin/index.html', {'stats': stats})


urlpatterns = [
    path('', root_redirect, name='root'),
    path('health/', health_check, name='health_check'),
    path('i18n/', include('django.conf.urls.i18n')),
    path('webhook/<str:token>/', telegram_webhook_view, name='telegram_webhook'),
    path('admin/dashboard/export/', admin.site.admin_view(dashboard_export_view), name='dashboard_export'),
    path('admin/dashboard/user/<int:user_id>/', admin.site.admin_view(user_detail_view), name='user_detail_page'),
    path('admin/dashboard/', admin.site.admin_view(dashboard_view), name='dashboard'),
    path('admin/send-dev-update/', admin.site.admin_view(admin_send_dev_update_view), name='admin_send_dev_update'),
    path('admin/backup-now/', admin.site.admin_view(admin_backup_now_view), name='admin_backup_now'),
    path('admin/backup-test/', admin.site.admin_view(admin_backup_test_view), name='admin_backup_test'),
    path('admin/logout/', admin_logout_view, name='admin_logout'),
    path('admin/', admin.site.urls),
    path('api/', include('core.urls')),
    path('jip-admin/', jip_admin_spa_view, name='jip_admin_spa'),
    path('jip-admin/<path:subpath>', jip_admin_spa_view, name='jip_admin_spa_sub'),
]

# WhiteNoise обрабатывает статические файлы автоматически через middleware
# Но в режиме DEBUG также добавляем явную обработку для надежности
if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    # Добавляем обработку статических файлов через Django (для разработки)
    urlpatterns += staticfiles_urlpatterns()
    # Для media файлов используем стандартный способ
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
