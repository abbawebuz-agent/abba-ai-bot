"""
Агрегаты для админ-дашборда (вкладки Umumiy / promo do'konlar / promo elektriklar).
"""
from __future__ import annotations

from collections import defaultdict
from typing import Any

from datetime import date, timedelta
from django.db.models import Count, Q, Sum
from django.db.models.functions import TruncDay
from django.utils import timezone
from django.utils.translation import get_language, gettext as _

from core.models import GiftRedemption, QRCode, TelegramUser, UzDistrict, UzRegion, PromoCodeAttempt
from core.regions import UZBEKISTAN_REGIONS

# Порядок строк как в ТЗ (коды как в core.regions / UzRegion)
DASHBOARD_REGION_ORDER = (
    'tashkent_city',
    'tashkent_region',
    'andijan',
    'fergana',
    'namangan',
    'jizzakh',
    'syrdarya',
    'samarkand',
    'bukhara',
    'navoi',
    'kashkadarya',
    'surkhandarya',
    'khorezm',
    'karakalpakstan',
)

_SPENT_EXCLUDE = ['rejected', 'cancelled_by_user', 'not_received']
_STATUS_TOPSHIRILGAN = ['completed']
_STATUS_JARAYONDA = ['pending', 'approved', 'sent']
_STATUS_TOPSHIRILMAGAN = ['rejected', 'not_received', 'cancelled_by_user']


def _region_name_localized(code: str) -> str:
    lang = get_language()[:2]
    r = UzRegion.objects.filter(code=code).first()
    if r:
        return (r.name_ru if lang == 'ru' and r.name_ru else r.name_uz)
    data = UZBEKISTAN_REGIONS.get(code) or {}
    return data.get('name_uz') or code


def _apply_qr_scan_date(qs, date_from, date_to):
    if date_from:
        qs = qs.filter(scanned_at__date__gte=date_from)
    if date_to:
        qs = qs.filter(scanned_at__date__lte=date_to)
    return qs


def _apply_redemption_date(qs, date_from, date_to):
    if date_from:
        qs = qs.filter(requested_at__date__gte=date_from)
    if date_to:
        qs = qs.filter(requested_at__date__lte=date_to)
    return qs


def _apply_qr_generated_date(qs, date_from, date_to):
    if date_from:
        qs = qs.filter(generated_at__date__gte=date_from)
    if date_to:
        qs = qs.filter(generated_at__date__lte=date_to)
    return qs


def compute_general_stats(date_from: date | None, date_to: date | None) -> dict[str, Any]:
    """Статистика для вкладки Umumiy (с фильтром дат и сравнением с прошлым периодом)."""
    
    # 0. Lifetime Statistics (Calculated once, independent of date filters)
    u_life = TelegramUser.objects.aggregate(
        total=Count('id'),
        e=Count('id', filter=Q(user_type='santenik')),
        s=Count('id', filter=Q(user_type='sotuvchi')),
        unselected=Count('id', filter=Q(user_type__isnull=True) | Q(user_type=''))
    )
    qr_life = QRCode.objects.filter(is_deleted=False).aggregate(
        # Electrician
        qr_e_total=Count('id', filter=Q(code_type='electrician')),
        qr_e_scanned=Count('id', filter=Q(code_type='santenik', is_scanned=True)),
        qr_e_unscanned=Count('id', filter=Q(code_type='santenik', is_scanned=False)),
        pool_e_scanned=Sum('points', filter=Q(code_type='santenik', is_scanned=True)),
        
        # Seller
        qr_s_total=Count('id', filter=Q(code_type='seller')),
        qr_s_scanned=Count('id', filter=Q(code_type='seller', is_scanned=True)),
        qr_s_unscanned=Count('id', filter=Q(code_type='seller', is_scanned=False)),
        pool_s_scanned=Sum('points', filter=Q(code_type='seller', is_scanned=True)),
    )
    
    life_gifts = GiftRedemption.objects.aggregate(
        total=Count('id'),
        e=Count('id', filter=Q(user__user_type='santenik')),
        s=Count('id', filter=Q(user__user_type='sotuvchi')),
        e_points=Sum('gift__points_cost', filter=Q(user__user_type='santenik') & ~Q(status__in=_SPENT_EXCLUDE)),
        s_points=Sum('gift__points_cost', filter=Q(user__user_type='sotuvchi') & ~Q(status__in=_SPENT_EXCLUDE)),
    )
    
    life_points_total = QRCode.objects.filter(is_deleted=False, is_scanned=True).aggregate(p=Sum('points'))['p'] or 0

    def get_stats_block(df: date | None, dt: date | None) -> dict[str, Any]:
        # 1. User Statistics (Filtered by period)
        user_qs = TelegramUser.objects.all()
        if df: user_qs = user_qs.filter(created_at__date__gte=df)
        if dt: user_qs = user_qs.filter(created_at__date__lte=dt)

        u_stats = user_qs.aggregate(
            total=Count('id'),
            e=Count('id', filter=Q(user_type='santenik')),
            s=Count('id', filter=Q(user_type='sotuvchi')),
            unselected=Count('id', filter=Q(user_type__isnull=True) | Q(user_type=''))
        )

        # 2. QR Code Statistics (Mixed: Scans in period, Totals from all time)
        qr_q = Q(is_deleted=False)
        q_scanned_period = Q(is_scanned=True)
        if df: q_scanned_period &= Q(scanned_at__date__gte=df)
        if dt: q_scanned_period &= Q(scanned_at__date__lte=dt)

        qr_stats = QRCode.objects.filter(qr_q).aggregate(
            # Electrician Counts
            qr_e_total=Count('id', filter=Q(code_type='electrician')),
            qr_e_scanned_life=Count('id', filter=Q(code_type='santenik', is_scanned=True)),
            qr_e_scanned_period=Count('id', filter=Q(code_type='electrician') & q_scanned_period),
            qr_e_unscanned=Count('id', filter=Q(code_type='santenik', is_scanned=False)),
            
            # Store Counts
            qr_s_total=Count('id', filter=Q(code_type='seller')),
            qr_s_scanned_life=Count('id', filter=Q(code_type='seller', is_scanned=True)),
            qr_s_scanned_period=Count('id', filter=Q(code_type='seller') & q_scanned_period),
            qr_s_unscanned=Count('id', filter=Q(code_type='seller', is_scanned=False)),
            
            # Points (Pool) - Scanned in period
            pool_e_scanned=Sum('points', filter=Q(code_type='electrician') & q_scanned_period),
            pool_s_scanned=Sum('points', filter=Q(code_type='seller') & q_scanned_period),
            
            # Lifetime Totals (for pool context if needed)
            pool_e_total=Sum('points', filter=Q(code_type='electrician')),
            pool_s_total=Sum('points', filter=Q(code_type='seller')),
        )

        # 3. Gift Redemption Statistics (Filtered by period)
        red_q = Q()
        if df: red_q &= Q(requested_at__date__gte=df)
        if dt: red_q &= Q(requested_at__date__lte=dt)

        # Base filters for spent calculations (not in exclude list)
        spent_q = ~Q(status__in=_SPENT_EXCLUDE)

        r_stats = GiftRedemption.objects.aggregate(
            pool_e_spent=Sum('gift__points_cost', filter=Q(user__user_type='santenik') & spent_q & red_q),
            pool_s_spent=Sum('gift__points_cost', filter=Q(user__user_type='sotuvchi') & spent_q & red_q),
            
            # Totals for Gift Requests Card
            gifts_e_total=Count('id', filter=Q(user__user_type='santenik') & red_q),
            gifts_s_total=Count('id', filter=Q(user__user_type='sotuvchi') & red_q),
            
            # Status Counts - Electrician
            re_top_c=Count('id', filter=Q(user__user_type='santenik', status__in=_STATUS_TOPSHIRILGAN) & red_q),
            re_jar_c=Count('id', filter=Q(user__user_type='santenik', status__in=_STATUS_JARAYONDA) & red_q),
            re_rej_c=Count('id', filter=Q(user__user_type='santenik', status__in=_STATUS_TOPSHIRILMAGAN) & red_q),

            # Status Counts - Seller
            rs_top_c=Count('id', filter=Q(user__user_type='sotuvchi', status__in=_STATUS_TOPSHIRILGAN) & red_q),
            rs_jar_c=Count('id', filter=Q(user__user_type='sotuvchi', status__in=_STATUS_JARAYONDA) & red_q),
            rs_rej_c=Count('id', filter=Q(user__user_type='sotuvchi', status__in=_STATUS_TOPSHIRILMAGAN) & red_q),

            # Specific Status Breakdown (Points) - Electrician
            re_top_p=Sum('gift__points_cost', filter=Q(user__user_type='santenik', status__in=_STATUS_TOPSHIRILGAN) & red_q),
            re_jar_p=Sum('gift__points_cost', filter=Q(user__user_type='santenik', status__in=_STATUS_JARAYONDA) & red_q),
            re_rej_p=Sum('gift__points_cost', filter=Q(user__user_type='santenik', status__in=_STATUS_TOPSHIRILMAGAN) & red_q),

            # Specific Status Breakdown (Points) - Seller
            rs_top_p=Sum('gift__points_cost', filter=Q(user__user_type='sotuvchi', status__in=_STATUS_TOPSHIRILGAN) & red_q),
            rs_jar_p=Sum('gift__points_cost', filter=Q(user__user_type='sotuvchi', status__in=_STATUS_JARAYONDA) & red_q),
            rs_rej_p=Sum('gift__points_cost', filter=Q(user__user_type='sotuvchi', status__in=_STATUS_TOPSHIRILMAGAN) & red_q),
        )

        return {
            'users_total': u_stats['total'],
            'users_electrician': u_stats['e'],
            'users_seller': u_stats['s'],
            'users_unselected': u_stats['unselected'],
            
            'qr_e_total': qr_stats['qr_e_total'],
            'qr_e_scanned': qr_stats['qr_e_scanned_period'],
            'qr_e_unscanned': qr_stats['qr_e_unscanned'],
            'life_qr_e_scanned': qr_stats['qr_e_scanned_life'],
            
            'qr_s_total': qr_stats['qr_s_total'],
            'qr_s_scanned': qr_stats['qr_s_scanned_period'],
            'qr_s_unscanned': qr_stats['qr_s_unscanned'],
            'life_qr_s_scanned': qr_stats['qr_s_scanned_life'],
            
            'points_total': (qr_stats['pool_e_scanned'] or 0) + (qr_stats['pool_s_scanned'] or 0),
            'points_electrician': qr_stats['pool_e_scanned'] or 0,
            'points_seller': qr_stats['pool_s_scanned'] or 0,
            
            'pool_e_total': qr_stats['pool_e_total'] or 0,
            'pool_e_scanned': qr_stats['pool_e_scanned'] or 0,
            'pool_e_spent': r_stats['pool_e_spent'] or 0,
            'pool_e_unscanned': (qr_stats['pool_e_total'] or 0) - (QRCode.objects.filter(code_type='santenik', is_scanned=True, is_deleted=False).aggregate(s=Sum('points'))['s'] or 0),
            
            'pool_s_total': qr_stats['pool_s_total'] or 0,
            'pool_s_scanned': qr_stats['pool_s_scanned'] or 0,
            'pool_s_spent': r_stats['pool_s_spent'] or 0,
            'pool_s_unscanned': (qr_stats['pool_s_total'] or 0) - (QRCode.objects.filter(code_type='seller', is_scanned=True, is_deleted=False).aggregate(s=Sum('points'))['s'] or 0),
            
            'gifts_total': (r_stats['gifts_e_total'] or 0) + (r_stats['gifts_s_total'] or 0),
            'gifts_electrician': r_stats['gifts_e_total'] or 0,
            'gifts_seller': r_stats['gifts_s_total'] or 0,
            
            'gift_redemptions_electrician': {
                'total_count': r_stats['gifts_e_total'] or 0,
                'total_points': (r_stats['re_top_p'] or 0) + (r_stats['re_jar_p'] or 0) + (r_stats['re_rej_p'] or 0),
                'topshirilgan': {'count': r_stats['re_top_c'] or 0, 'points': r_stats['re_top_p'] or 0},
                'jarayonda': {'count': r_stats['re_jar_c'] or 0, 'points': r_stats['re_jar_p'] or 0},
                'topshirilmagan': {'count': r_stats['re_rej_c'] or 0, 'points': r_stats['re_rej_p'] or 0},
            },
            'gift_redemptions_seller': {
                'total_count': r_stats['gifts_s_total'] or 0,
                'total_points': (r_stats['rs_top_p'] or 0) + (r_stats['rs_jar_p'] or 0) + (r_stats['rs_rej_p'] or 0),
                'topshirilgan': {'count': r_stats['rs_top_c'] or 0, 'points': r_stats['rs_top_p'] or 0},
                'jarayonda': {'count': r_stats['rs_jar_c'] or 0, 'points': r_stats['rs_jar_p'] or 0},
                'topshirilmagan': {'count': r_stats['rs_rej_c'] or 0, 'points': r_stats['rs_rej_p'] or 0},
            },
        }

    # 1. Current Stats
    curr = get_stats_block(date_from, date_to)

    # 2. Previous Period Stats (for trends)
    # BUG FIX: Do NOT override curr here! The else branch previously
    # replaced all-time curr with a 30-day window, breaking preset=all.
    prev_df = prev_dt = None
    if date_from and date_to:
        delta = date_to - date_from
        prev_dt = date_from - timedelta(days=1)
        prev_df = prev_dt - delta
    else:
        # For all-time or partial date filter, compare against last 30 days
        # for trend context — but do NOT touch curr.
        now = timezone.now().date()
        prev_dt = now - timedelta(days=1)
        prev_df = prev_dt - timedelta(days=29)

    prev = get_stats_block(prev_df, prev_dt)

    # 3. Compute Trends
    def pct_change(curr_val, prev_val):
        if prev_val == 0:
            return 100 if curr_val > 0 else 0
        return round(((curr_val - prev_val) / prev_val) * 100, 1)

    trends = {
        'users_total': pct_change(curr['users_total'], prev['users_total']),
        'points_total': pct_change(curr['points_total'], prev['points_total']),
    }

    curr['trends'] = trends
    
    # 4. Inject Lifetime Statistics
    curr['life_u_total'] = u_life['total']
    curr['life_u_e'] = u_life['e']
    curr['life_u_s'] = u_life['s']
    curr['life_u_unselected'] = u_life['unselected']
    
    curr['life_qr_e_total'] = qr_life['qr_e_total']
    curr['life_qr_e_scanned'] = qr_life['qr_e_scanned']
    curr['life_qr_e_unscanned'] = qr_life['qr_e_unscanned']
    
    curr['life_qr_s_total'] = qr_life['qr_s_total']
    curr['life_qr_s_scanned'] = qr_life['qr_s_scanned']
    curr['life_qr_s_unscanned'] = qr_life['qr_s_unscanned']
    
    curr['life_pool_e_scanned'] = qr_life['pool_e_scanned'] or 0
    curr['life_pool_s_scanned'] = qr_life['pool_s_scanned'] or 0
    
    curr['life_gifts_total'] = life_gifts['total']
    curr['life_gifts_e'] = life_gifts['e']
    curr['life_gifts_s'] = life_gifts['s']
    curr['life_pool_s_spent'] = life_gifts['s_points'] or 0
    curr['life_pool_e_spent'] = life_gifts['e_points'] or 0
    
    curr['life_points_total'] = life_points_total

    return curr


def _promo_metrics_for_scope(
    user_type: str,
    date_from: date | None,
    date_to: date | None,
    region_id: int | None | str,
    district_id: int | None | str,
    exclude_region_ids: list[int] | None = None,
) -> dict[str, int]:
    """
    Returns a dict with lifetime and period metrics for the given scope.
    Special cases:
      - region_id='isnull': region_id__isnull=True
      - region_id='undefined': (region_id__isnull=True OR region_id__notin=exclude_region_ids)
      - district_id='isnull': district_id__isnull=True
    """
    # 1. Users (Lifetime as primary, Period as delta)
    # NOTE: We do NOT filter by is_active=True here to match general dashboard totals
    uq = TelegramUser.objects.filter(user_type=user_type)
    
    if region_id == 'isnull':
        uq = uq.filter(region_id__isnull=True)
    elif region_id == 'undefined':
        q_undef = Q(region_id__isnull=True)
        if exclude_region_ids:
            q_undef |= ~Q(region_id__in=exclude_region_ids)
        uq = uq.filter(q_undef)
    elif region_id is not None:
        uq = uq.filter(region_id=region_id)
    
    if district_id == 'isnull':
        uq = uq.filter(district_id__isnull=True)
    elif district_id is not None:
        uq = uq.filter(district_id=district_id)
    
    users_life = uq.count()
    
    # New users in period
    uq_period = uq
    if date_from: uq_period = uq_period.filter(created_at__date__gte=date_from)
    if date_to: uq_period = uq_period.filter(created_at__date__lte=date_to)
    users_period = uq_period.count()

    # 2. QR Codes / Points
    code_type = user_type  # 'electrician' or 'seller'
    qr_base = QRCode.objects.filter(
        is_scanned=True, code_type=code_type, is_deleted=False,
    )
    
    if region_id == 'isnull':
        qr_base = qr_base.filter(scanned_by__region_id__isnull=True)
    elif region_id == 'undefined':
        q_undef = Q(scanned_by__region_id__isnull=True)
        if exclude_region_ids:
            q_undef |= ~Q(scanned_by__region_id__in=exclude_region_ids)
        qr_base = qr_base.filter(q_undef)
    elif region_id is not None:
        qr_base = qr_base.filter(scanned_by__region_id=region_id)
        
    if district_id == 'isnull':
        qr_base = qr_base.filter(scanned_by__district_id__isnull=True)
    elif district_id is not None:
        qr_base = qr_base.filter(scanned_by__district_id=district_id)
    
    # Lifetime Scanned
    qr_life = qr_base.aggregate(c=Count('id'), p=Sum('points'))
    cards_life = qr_life['c'] or 0
    points_life = qr_life['p'] or 0
    
    # Period Scanned
    qr_period = _apply_qr_scan_date(qr_base, date_from, date_to)
    qr_period_stats = qr_period.aggregate(c=Count('id'), p=Sum('points'))
    cards_period = qr_period_stats['c'] or 0
    points_period = qr_period_stats['p'] or 0

    # 3. Spent Points (Redemptions)
    spent_q = ~Q(status__in=_SPENT_EXCLUDE)
    red_base = GiftRedemption.objects.filter(user__user_type=user_type).filter(spent_q)
    
    if region_id == 'isnull':
        red_base = red_base.filter(user__region_id__isnull=True)
    elif region_id == 'undefined':
        q_undef = Q(user__region_id__isnull=True)
        if exclude_region_ids:
            q_undef |= ~Q(user__region_id__in=exclude_region_ids)
        red_base = red_base.filter(q_undef)
    elif region_id is not None:
        red_base = red_base.filter(user__region_id=region_id)
        
    if district_id == 'isnull':
        red_base = red_base.filter(user__district_id__isnull=True)
    elif district_id is not None:
        red_base = red_base.filter(user__district_id=district_id)
    
    # Lifetime Spent
    spent_life = red_base.aggregate(s=Sum('gift__points_cost'))['s'] or 0
    
    # Period Spent
    red_period = _apply_redemption_date(red_base, date_from, date_to)
    spent_period = red_period.aggregate(s=Sum('gift__points_cost'))['s'] or 0

    return {
        'u_life': users_life,
        'u_period': users_period,
        'c_life': cards_life,
        'c_period': cards_period,
        'p_life': points_life,
        'p_period': points_period,
        's_life': spent_life,
        's_period': spent_period,
    }


def build_promo_table_rows(
    user_type: str,
    date_from,
    date_to,
    drill_region: UzRegion | None,
    global_stats: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    """
    Строки таблицы «Aksiyada ishtirok…»: по вилоятам или по туманам при drill_region.
    
    BUG FIX: When a date filter is active, the primary values in the table
    should reflect the filtered period, not all-time totals.
    """
    rows: list[dict[str, Any]] = []
    # Totals accumulate based on what's being filtered
    is_filtered = bool(date_from or date_to)
    total_u = total_c = total_p = total_s = 0
    total_u_life = total_c_life = total_p_life = total_sl = 0

    if drill_region is None:
        regions_by_code = {r.code: r for r in UzRegion.objects.all()}
        listed_ids = [r.pk for r in regions_by_code.values() if r.code in DASHBOARD_REGION_ORDER]
        for code in DASHBOARD_REGION_ORDER:
            reg = regions_by_code.get(code)
            name = _region_name_localized(code)
            if reg is None:
                rows.append(
                    {
                        'code': code,
                        'name': name,
                        'users': 0,
                        'users_life': 0,
                        'cards': 0,
                        'cards_life': 0,
                        'points': 0,
                        'points_life': 0,
                        'is_filtered': is_filtered,
                        'drill': False,
                        'is_total': False,
                    }
                )
                continue
            m = _promo_metrics_for_scope(
                user_type, date_from, date_to, reg.pk, None
            )
            # When filtered: primary = period values; secondary = all-time
            # When not filtered (all-time): primary = all-time; no secondary needed
            rows.append(
                {
                    'code': code,
                    'name': name,
                    'users': m['u_period'] if is_filtered else m['u_life'],
                    'users_life': m['u_life'],
                    'cards': m['c_period'] if is_filtered else m['c_life'],
                    'cards_life': m['c_life'],
                    'points': m['p_period'] if is_filtered else m['p_life'],
                    'points_life': m['p_life'],
                    'spent': m['s_period'] if is_filtered else m['s_life'],
                    'spent_life': m['s_life'],
                    'is_filtered': is_filtered,
                    'drill': True,
                    'is_total': False,
                }
            )
            # Sum up the correct primary values for TOTAL row
            total_u += m['u_period'] if is_filtered else m['u_life']
            total_c += m['c_period'] if is_filtered else m['c_life']
            total_p += m['p_period'] if is_filtered else m['p_life']
            total_u_life += m['u_life']
            total_c_life += m['c_life']
            total_p_life += m['p_life']
            total_s += m['s_period'] if is_filtered else m['s_life']
            total_sl += m['s_life']
            
        # BUG FIX: Add "Undefined" (Noma'lum) row for all users NOT in the listed regions
        # This includes region_id IS NULL and any region_id not in listed_ids
        m_undef = _promo_metrics_for_scope(
            user_type, date_from, date_to, 'undefined', None, exclude_region_ids=listed_ids
        )
        if m_undef['u_life'] > 0 or m_undef['c_life'] > 0:
            rows.append(
                {
                    'code': 'undefined',
                    'name': _("Noma'lum"),
                    'users': m_undef['u_period'] if is_filtered else m_undef['u_life'],
                    'users_life': m_undef['u_life'],
                    'cards': m_undef['c_period'] if is_filtered else m_undef['c_life'],
                    'cards_life': m_undef['c_life'],
                    'points': m_undef['p_period'] if is_filtered else m_undef['p_life'],
                    'points_life': m_undef['p_life'],
                    'spent': m_undef['s_period'] if is_filtered else m_undef['s_life'],
                    'spent_life': m_undef['s_life'],
                    'is_filtered': is_filtered,
                    'drill': False,
                    'is_total': False,
                }
            )
            total_u += m_undef['u_period'] if is_filtered else m_undef['u_life']
            total_c += m_undef['c_period'] if is_filtered else m_undef['c_life']
            total_p += m_undef['p_period'] if is_filtered else m_undef['p_life']
            total_u_life += m_undef['u_life']
            total_c_life += m_undef['c_life']
            total_p_life += m_undef['p_life']
            total_s += m_undef['s_period'] if is_filtered else m_undef['s_life']
            total_sl += m_undef['s_life']
    else:
        d_map_local: dict[int | None, dict] = defaultdict(
            lambda: {'users': 0, 'cards': 0, 'points': 0}
        )

        district_objs = list(
            UzDistrict.objects.filter(region=drill_region).order_by('code')
        )
        seen: set[int | None] = {None}
        ordered_ids: list[int | None] = [None]
        for d in district_objs:
            ordered_ids.append(d.pk)
            seen.add(d.pk)
        # Also include any district_ids that have stats but aren't in ordered list
        u_rows_all = (
            TelegramUser.objects.filter(
                user_type=user_type,
                is_active=True,
                region_id=drill_region.pk,
            )
            .values('district_id')
            .annotate(c=Count('id'))
        )
        for row in u_rows_all:
            if row['district_id'] not in seen:
                ordered_ids.append(row['district_id'])
                seen.add(row['district_id'])

        d_map = {d.pk: d for d in district_objs}
        lang = get_language()[:2]
        for did in ordered_ids:
            # BUG FIX: For did=None, filter specifically for district_id__isnull=True
            # to avoid duplicate counting of the entire region total.
            target_did = did if did is not None else 'isnull'
            m = _promo_metrics_for_scope(
                user_type, date_from, date_to, drill_region.pk, target_did
            )
            
            if did is None:
                name = _('Tuman tanlanmagan')
                code = ''
            else:
                d_obj = d_map.get(did)
                if d_obj:
                    name = d_obj.name_ru if lang == 'ru' and d_obj.name_ru else d_obj.name_uz
                else:
                    name = str(did)
                code = d_obj.code if d_obj else ''

            # Only add row if it has any stats (to keep drilldown clean)
            if m['u_life'] > 0 or m['c_life'] > 0:
                rows.append(
                    {
                        'code': code,
                        'district_id': did,
                        'name': name,
                        'users': m['u_period'] if is_filtered else m['u_life'],
                        'users_life': m['u_life'],
                        'cards': m['c_period'] if is_filtered else m['c_life'],
                        'cards_life': m['c_life'],
                        'points': m['p_period'] if is_filtered else m['p_life'],
                        'points_life': m['p_life'],
                        'spent': m['s_period'] if is_filtered else m['s_life'],
                        'spent_life': m['s_life'],
                        'is_filtered': is_filtered,
                        'drill': False,
                        'is_total': False,
                    }
                )
                total_u += m['u_period'] if is_filtered else m['u_life']
                total_c += m['c_period'] if is_filtered else m['c_life']
                total_p += m['p_period'] if is_filtered else m['p_life']
                total_u_life += m['u_life']
                total_c_life += m['c_life']
                total_p_life += m['p_life']
                total_s += m['s_period'] if is_filtered else m['s_life']
                total_sl += m['s_life']

    # Final Totals: Use global_stats if provided to ensure exact matching with cards
    if global_stats:
        gs = global_stats
        if user_type == 'sotuvchi':
            res_u = gs.get('life_u_s', total_u_life)
            res_up = gs.get('users_seller', total_u)
            res_c = gs.get('life_qr_s_scanned', total_c_life)
            res_cp = gs.get('qr_s_scanned', total_c) # Period count
            res_p = gs.get('life_pool_s_scanned', total_p_life)
            res_pp = gs.get('pool_s_scanned', total_p) # Period points
            res_s = gs.get('pool_s_spent', total_s)
            res_sl = gs.get('life_pool_s_spent', total_sl)
        else:
            res_u = gs.get('life_u_e', total_u_life)
            res_up = gs.get('users_electrician', total_u)
            res_c = gs.get('life_qr_e_scanned', total_c_life)
            res_cp = gs.get('qr_e_scanned', total_c)
            res_p = gs.get('life_pool_e_scanned', total_p_life)
            res_pp = gs.get('points_electrician', total_p)
            res_s = gs.get('pool_e_spent', total_s)
            res_sl = gs.get('life_pool_e_spent', total_sl)
        
        total_rows = {
            'users': res_up if is_filtered else res_u,
            'users_life': res_u,
            'cards': res_cp if is_filtered else res_c,
            'cards_life': res_c,
            'points': res_pp if is_filtered else res_p,
            'points_life': res_p,
            'spent': res_s,
            'spent_life': res_sl,
        }
    else:
        # Fallback to calculated totals from visible rows
        total_rows = {
            'users': total_u,
            'users_life': total_u_life,
            'cards': total_c,
            'cards_life': total_c_life,
            'points': total_p,
            'points_life': total_p_life,
            'spent': 0, # Not summed up currently
            'spent_life': 0,
        }

    rows.append(
        {
            'code': '',
            'name': _('TOTAL'),
            'users': total_rows['users'],
            'users_life': total_rows['users_life'],
            'cards': total_rows['cards'],
            'cards_life': total_rows['cards_life'],
            'points': total_rows['points'],
            'points_life': total_rows['points_life'],
            'spent': total_rows['spent'],
            'spent_life': total_rows['spent_life'],
            'is_filtered': is_filtered,
            'drill': False,
            'is_total': True,
        }
    )
    return rows

def compute_intelligence_stats(date_from, date_to) -> dict[str, Any]:
    """
    Advanced behavioral & fraud analytics:
    - Promo code attempt metrics (Success vs. Failure)
    - User segmentation by integrity
    - Suspicious activity leaderboard
    """
    now = timezone.now()
    
    # Base Queryset for Attempts
    att_qs_life = PromoCodeAttempt.objects.all()
    
    att_qs_period = att_qs_life
    if date_from:
        att_qs_period = att_qs_period.filter(attempted_at__date__gte=date_from)
    if date_to:
        att_qs_period = att_qs_period.filter(attempted_at__date__lte=date_to)

    # 1. Attempt Distribution (Fraud context)
    total_att_life = att_qs_life.count()
    success_att_life = att_qs_life.filter(is_successful=True).count()
    failed_att_life = total_att_life - success_att_life
    
    total_att_period = att_qs_period.count()
    success_att_period = att_qs_period.filter(is_successful=True).count()
    failed_att_period = total_att_period - success_att_period

    # 2. QR Code Activation Consistency (Actual Business Metric)
    # Alignment with General tab: Use QRCode directly for "Successful scans"
    qr_life_q = QRCode.objects.filter(is_deleted=False)
    total_qr_life = qr_life_q.count()
    success_qr_life = qr_life_q.filter(is_scanned=True).count()

    qr_period_q = qr_life_q
    if date_from: qr_period_q = qr_period_q.filter(scanned_at__date__gte=date_from)
    if date_to: qr_period_q = qr_period_q.filter(scanned_at__date__lte=date_to)
    success_qr_period = qr_period_q.filter(is_scanned=True).count()
    
    success_rate_life = (success_att_life / total_att_life * 100) if total_att_life > 0 else 0
    success_rate_period = (success_att_period / total_att_period * 100) if total_att_period > 0 else 0

    # 3. User Segmentation by Failure Count (Integrity)
    # This identifies "Brute-force" or "Guessing" behavior clusters
    # BUG FIX: Ensure segments are mutually exclusive by excluding already blocked users from others
    blocked_qs = TelegramUser.objects.filter(promo_blocked_until__gt=now, is_active=True)
    blocked_count = blocked_qs.count()
    
    other_active = TelegramUser.objects.filter(is_active=True).exclude(promo_blocked_until__gt=now)
    
    integrity_segments = {
        'clean': other_active.filter(promo_failed_attempts=0).count(),
        'warning': other_active.filter(promo_failed_attempts__range=(1, 2)).count(),
        'suspicious': other_active.filter(promo_failed_attempts__gte=3).count(),
        'blocked': blocked_count,
    }

    # 3. Suspicious Activity Leaderboard (Top 10 by failures)
    # BUG FIX: Handle None names in suspicious_leaderboard
    suspicious_leaderboard_raw = list(
        TelegramUser.objects.filter(promo_failed_attempts__gt=0)
        .values('id', 'first_name', 'last_name', 'username', 'phone_number', 'promo_failed_attempts')
        .order_by('-promo_failed_attempts')[:10]
    )
    
    suspicious_leaderboard = []
    for user in suspicious_leaderboard_raw:
        # Pre-process names to avoid literal "None" in templates
        user['first_name'] = user['first_name'] or ""
        user['last_name'] = user['last_name'] or ""
        suspicious_leaderboard.append(user)

    # 4. Source Distribution (Where are they entering codes?)
    sources = att_qs_period.values('source').annotate(count=Count('id')).order_by('-count')
    source_stats = {s['source']: s['count'] for s in sources}

    # 5. Daily Anomaly Trend (Failed vs Success)
    # This helps identify coordinated brute-force spikes
    end_date = date_to or now.date()
    
    if not date_from:
        labels = [str(_('Barcha vaqt'))]
        success_data = [success_att_life]
        failed_data = [failed_att_life]
        
        first_att = PromoCodeAttempt.objects.order_by('attempted_at').first()
        all_time_start = first_att.attempted_at.date() if first_att else end_date
        delta = end_date - all_time_start
    else:
        start_date = date_from
        at_trends = (
            att_qs_period.filter(attempted_at__date__range=(start_date, end_date))
            .annotate(day=TruncDay('attempted_at'))
            .values('day', 'is_successful')
            .annotate(count=Count('id'))
            .order_by('day')
        )
        
        delta = end_date - start_date
        date_list = [start_date + timedelta(days=i) for i in range(delta.days + 1)]
        labels = [d.strftime('%d.%m') for d in date_list]
        
        success_trend = {d: 0 for d in date_list}
        failed_trend = {d: 0 for d in date_list}
        
        for t in at_trends:
            d = t['day'].date()
            if t['is_successful']:
                success_trend[d] = t['count']
            else:
                failed_trend[d] = t['count']
                
        success_data = [success_trend[d] for d in date_list]
        failed_data = [failed_trend[d] for d in date_list]

    # 5. Summary Metrics for UI
    clean_perc = (integrity_segments['clean'] / TelegramUser.objects.filter(is_active=True).count() * 100) if TelegramUser.objects.filter(is_active=True).count() > 0 else 0
    avg_daily_fail = failed_att_period / (delta.days + 1) if delta.days >= 0 else 0

    return {
        'total_qrcodes_life': total_qr_life,
        'success_attempts_life': success_qr_life,
        'failed_attempts_life': failed_att_life,
        'success_rate_life': round(success_rate_life, 1),
        
        'success_attempts': success_qr_period,
        'failed_attempts': failed_att_period,
        'success_rate': round(success_rate_period, 1),
        
        'total_attempts_life': total_att_life,
        'total_attempts': total_att_period,
        'clean_percentage': round(clean_perc, 1),
        'avg_daily_failures': round(avg_daily_fail, 1),
        'segments': integrity_segments,
        'leaderboard': suspicious_leaderboard,
        'sources': source_stats,
        'trends': {
            'labels': labels,
            'success': success_data,
            'failed': failed_data,
        }
    }

def compute_dashboard_charts(date_from, date_to, drill_region=None) -> dict[str, Any]:
    """Данные для графиков (Chart.js)."""
    # Определяем диапазон для трендов (по умолчанию последние 30 дней)
    end_date = date_to or timezone.now().date()
    
    if not date_from:
        labels = [str(_('Barcha vaqt'))]
        
        reg_series = [TelegramUser.objects.count()]
        
        qr_stats = QRCode.objects.filter(is_scanned=True, is_deleted=False).aggregate(count=Count('id'), pts=Sum('points'))
        act_series = [qr_stats['count'] or 0]
        act_pts_series = [qr_stats['pts'] or 0]
        
        red_stats = GiftRedemption.objects.exclude(status__in=_SPENT_EXCLUDE).aggregate(count=Count('id'), pts=Sum('gift__points_cost'))
        red_series = [red_stats['count'] or 0]
        red_pts_series = [red_stats['pts'] or 0]
        
        first_user = TelegramUser.objects.order_by('created_at').first()
        start_date = first_user.created_at.date() if first_user else (end_date - timedelta(days=29))
    else:
        start_date = date_from
        
        # 1. Тренды регистраций
        reg_trends = (
            TelegramUser.objects.filter(created_at__date__range=(start_date, end_date))
            .annotate(day=TruncDay('created_at'))
            .values('day')
            .annotate(count=Count('id'))
            .order_by('day')
        )
        
        # 2. Тренды активаций
        act_trends = (
            QRCode.objects.filter(is_scanned=True, is_deleted=False, scanned_at__date__range=(start_date, end_date))
            .annotate(day=TruncDay('scanned_at'))
            .values('day')
            .annotate(count=Count('id'), pts=Sum('points'))
            .order_by('day')
        )
        
        # 3. Тренды выкупа (Redemptions)
        red_trends = (
            GiftRedemption.objects.filter(requested_at__date__range=(start_date, end_date))
            .exclude(status__in=_SPENT_EXCLUDE)
            .annotate(day=TruncDay('requested_at'))
            .values('day')
            .annotate(count=Count('id'), pts=Sum('gift__points_cost'))
            .order_by('day')
        )
    
        # Формируем список всех дат в диапазоне для консистентности графиков
        delta = end_date - start_date
        date_list = [start_date + timedelta(days=i) for i in range(delta.days + 1)]
        labels = [d.strftime('%d.%m') for d in date_list]
        
        def fill_series(trends, key='count'):
            data_map = {t['day'].date(): t[key] for t in trends}
            return [data_map.get(d, 0) for d in date_list]
            
        reg_series = fill_series(reg_trends)
        act_series = fill_series(act_trends)
        act_pts_series = fill_series(act_trends, 'pts')
        red_series = fill_series(red_trends)
        red_pts_series = fill_series(red_trends, 'pts')

    # 4. Популярность подарков (Топ 5)
    gift_popularity = (
        GiftRedemption.objects.values('gift__name_uz_latin', 'gift__name_ru')
        .annotate(count=Count('id'))
        .order_by('-count')[:5]
    )
    lang = get_language()[:2]
    gift_labels = [
        (g['gift__name_ru'] if lang == 'ru' and g['gift__name_ru'] else g['gift__name_uz_latin'])
        for g in gift_popularity
    ]
    gift_data = [g['count'] for g in gift_popularity]

    # 5. Региональное распределение (Топ 7 для графика)
    reg_dist = (
        TelegramUser.objects.filter(region__isnull=False)
        .values('region__code', 'region__name_uz', 'region__name_ru')
        .annotate(count=Count('id'))
        .order_by('-count')[:7]
    )
    reg_labels = [
        (r['region__name_ru'] if lang == 'ru' and r['region__name_ru'] else r['region__name_uz'])
        for r in reg_dist
    ]
    reg_data = [r['count'] for r in reg_dist]

    # 6. Данные для карты (Все регионы)
    # Считаем активации в периоде по регионам
    map_stats = (
        QRCode.objects.filter(is_scanned=True, scanned_at__date__range=(start_date, end_date))
        .values('scanned_by__region__code')
        .annotate(scans=Count('id'))
    )
    # Считаем общее кол-во пользователей по регионам
    map_users = (
        TelegramUser.objects.filter(region__isnull=False)
        .values('region__code')
        .annotate(users=Count('id'))
    )
    
    map_data = {}
    for code in DASHBOARD_REGION_ORDER:
        name = _region_name_localized(code)
        scans = 0
        users = 0
        
        # Находим данные по сканам
        ms_match = next((ms for ms in map_stats if ms['scanned_by__region__code'] == code), None)
        if ms_match:
            scans = ms_match['scans']
            
        # Находим данные по пользователям
        mu_match = next((mu for mu in map_users if mu['region__code'] == code), None)
        if mu_match:
            users = mu_match['users']
            
        map_data[code] = {
            'name': name,
            'scans': scans,
            'users': users
        }

    # 7. Распределение заявок по статусам (Lifetime distribution)
    status_counts_map = {
        item['status']: item['count'] 
        for item in GiftRedemption.objects.values('status')
        .annotate(count=Count('id'))
    }
    
    status_labels = []
    status_data = []
    
    # Iterate through ALL choices to include zero-count statuses
    for status_code, label in GiftRedemption.STATUS_CHOICES:
        # Translate or at least use the default label
        status_labels.append(str(label))
        status_data.append(status_counts_map.get(status_code, 0))

    # 8. Redemption Geography (New: By Region or District)
    geo_qs = GiftRedemption.objects.filter(requested_at__date__range=(start_date, end_date))
    if drill_region:
        geo_dist = (
            geo_qs.filter(user__region=drill_region)
            .values('user__district__name_uz', 'user__district__name_ru')
            .annotate(count=Count('id'))
            .order_by('-count')
        )
        geo_labels = [
            (r['user__district__name_ru'] if lang == 'ru' and r['user__district__name_ru'] else r['user__district__name_uz']) or _('Other')
            for r in geo_dist
        ]
    else:
        geo_dist = (
            geo_qs.values('user__region__name_uz', 'user__region__name_ru')
            .annotate(count=Count('id'))
            .order_by('-count')
        )
        geo_labels = [
            (r['user__region__name_ru'] if lang == 'ru' and r['user__region__name_ru'] else r['user__region__name_uz']) or _('Other')
            for r in geo_dist
        ]
    geo_data = [r['count'] for r in geo_dist]

    # 9. New vs Returning Users
    # We define "Active" users in the period [date_from, date_to]
    # If no period, default to last 30 days for this specific metric
    calc_from = date_from
    calc_to = date_to or timezone.now().date()
    if not calc_from:
        calc_from = calc_to - timedelta(days=29)

    # 1. Total Active Users in this period (Users who did something)
    active_in_period_ids = set()
    
    # Activity from Scans
    active_in_period_ids.update(
        QRCode.objects.filter(
            scanned_at__date__range=(calc_from, calc_to),
            scanned_by__isnull=False
        ).values_list('scanned_by_id', flat=True)
    )
    # Activity from Promo attempts
    active_in_period_ids.update(
        PromoCodeAttempt.objects.filter(
            attempted_at__date__range=(calc_from, calc_to),
            user__isnull=False
        ).values_list('user_id', flat=True)
    )
    # Activity from Redemptions
    active_in_period_ids.update(
        GiftRedemption.objects.filter(
            requested_at__date__range=(calc_from, calc_to),
            user__isnull=False
        ).values_list('user_id', flat=True)
    )
    
    # Remove None if it slipped in
    active_in_period_ids.discard(None)
    
    # 2. Split them into New (registered in period) and Returning (registered before)
    new_users_count = TelegramUser.objects.filter(
        id__in=active_in_period_ids,
        created_at__date__range=(calc_from, calc_to)
    ).count()
    
    returning_users_count = TelegramUser.objects.filter(
        id__in=active_in_period_ids,
        created_at__date__lt=calc_from
    ).count()

    return {
        'labels': labels,
        'reg_series': reg_series,
        'act_series': act_series,
        'act_pts_series': act_pts_series,
        'red_series': red_series,
        'red_pts_series': red_pts_series,
        'gift_labels': gift_labels,
        'gift_data': gift_data,
        'reg_labels': reg_labels,
        'reg_data': reg_data,
        'map_data': map_data,
        'redemption_status_labels': status_labels,
        'redemption_status_data': status_data,
        'redemption_geo_labels': geo_labels,
        'redemption_geo_data': geo_data,
        'is_drilldown': drill_region is not None,
        'retention': {
            'new_users': new_users_count,
            'returning_users': returning_users_count,
            'total_active': new_users_count + returning_users_count
        }
    }



def get_user_crm_details(user_id: int) -> dict[str, Any] | None:
    """Detailed CRM behavior for a specific user (AJAX)."""
    user = TelegramUser.objects.filter(pk=user_id).select_related('region', 'district').first()
    if not user:
        return None

    # 1. Basic Stats
    total_scans_qs = QRCode.objects.filter(scanned_by=user, is_scanned=True, is_deleted=False)
    total_scans = total_scans_qs.count()
    total_earned = total_scans_qs.aggregate(t=Sum('points'))['t'] or 0
    total_spent = GiftRedemption.objects.filter(user=user).exclude(status__in=_SPENT_EXCLUDE).aggregate(
        t=Sum('gift__points_cost')
    )['t'] or 0
    
    # Failed attempts for fraud detection
    failed_attempts_qs = PromoCodeAttempt.objects.filter(user=user, is_successful=False).order_by('-attempted_at')
    failed_count = failed_attempts_qs.count()

    # 2. Activity Trends (Last 14 days)
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=13)
    scan_trends = (
        QRCode.objects.filter(scanned_by=user, is_scanned=True, scanned_at__date__range=(start_date, end_date))
        .annotate(day=TruncDay('scanned_at'))
        .values('day')
        .annotate(count=Count('id'))
        .order_by('day')
    )
    
    delta = end_date - start_date
    date_list = [start_date + timedelta(days=i) for i in range(delta.days + 1)]
    trend_map = {t['day'].date(): t['count'] for t in scan_trends}
    trend_data = [trend_map.get(d, 0) for d in date_list]
    trend_labels = [d.strftime('%d.%m') for d in date_list]

    # 3. Recent Scans (Upped to 50 for "all logs" feel)
    recent_scans = (
        QRCode.objects.filter(scanned_by=user, is_scanned=True)
        .order_by('-scanned_at')[:50]
        .values('code', 'points', 'scanned_at')
    )

    # 4. Recent Gift Requests (Upped to 50)
    recent_redemptions = (
        GiftRedemption.objects.filter(user=user)
        .order_by('-requested_at')[:50]
        .values('gift__name_uz_latin', 'gift__name_ru', 'status', 'requested_at', 'gift__points_cost')
    )
    
    # 5. Failed Attempts Log
    recent_failed = failed_attempts_qs[:20].values('raw_code', 'attempted_at', 'source')

    lang = get_language()[:2]
    
    is_blocked, block_type, blocked_until = user.is_promo_code_blocked()
    
    return {
        'id': user.pk,
        'telegram_id': user.telegram_id,
        'full_name': f"{user.first_name or ''} {user.last_name or ''}".strip() or user.username or f"User {user.pk}",
        'username': user.username or '-',
        'phone': user.phone_number or '-',
        'user_type': user.user_type,
        'language_code': user.language,
        'region': (user.region.name_ru if lang == 'ru' and user.region.name_ru else user.region.name_uz) if user.region else '-',
        'district': (user.district.name_ru if lang == 'ru' and user.district.name_ru else user.district.name_uz) if user.district else '-',
        'points_balance': user.points,
        'points_earned_lifetime': total_earned,
        'points_spent': total_spent,
        'total_scans': total_scans,
        'failed_attempts_count': failed_count,
        'is_blocked': is_blocked,
        'block_type': block_type,
        'blocked_until': blocked_until.strftime('%d.%m.%Y %H:%M') if blocked_until else None,
        'smartup_id': user.smartup_id or '-',
        'last_message_sent_at': user.last_message_sent_at.strftime('%d.%m.%Y %H:%M') if user.last_message_sent_at else None,
        'blocked_bot_at': user.blocked_bot_at.strftime('%d.%m.%Y %H:%M') if user.blocked_bot_at else None,
        'privacy_accepted': user.privacy_accepted,
        'latitude': user.latitude,
        'longitude': user.longitude,
        'created_at': user.created_at.strftime('%d.%m.%Y %H:%M'),
        'updated_at': user.updated_at.strftime('%d.%m.%Y %H:%M'),
        'trends': {
            'labels': trend_labels,
            'data': trend_data,
        },
        'recent_scans': [
            {
                'code': s['code'],
                'points': s['points'],
                'date': s['scanned_at'].strftime('%d.%m.%Y %H:%M'),
            } for s in recent_scans
        ],
        'recent_redemptions': [
            {
                'name': (r['gift__name_ru'] if lang == 'ru' and r['gift__name_ru'] else r['gift__name_uz_latin']),
                'status': r['status'],
                'status_display': dict(GiftRedemption.STATUS_CHOICES).get(r['status'], r['status']),
                'points': r['gift__points_cost'],
                'date': r['requested_at'].strftime('%d.%m.%Y %H:%M'),
            } for r in recent_redemptions
        ],
        'failed_logs': [
            {
                'code': f['raw_code'] or '—',
                'date': f['attempted_at'].strftime('%d.%m.%Y %H:%M'),
                'source': f['source'],
            } for f in recent_failed
        ]
    }
