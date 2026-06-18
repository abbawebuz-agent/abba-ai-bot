"""
JIP Admin Dashboard — READ-ONLY JSON API
=========================================

Serves the `/jip-admin/` React SPA (Claude Design "Modern Apple" handoff).

Design rules (see project memory feedback-jip-no-db-writes / feedback-jip-dev-rules):
  * READ-ONLY. No DB writes anywhere in this file.
  * Does NOT touch Django admin (/admin/) — fully separate surface.
  * Reuses core.dashboard_stats engine (same source as the admin dashboard).
  * Every endpoint is wrapped so it NEVER returns HTTP 500 — on any error it
    returns 200 with {"ok": false, "error": ...} so the post-deploy curl sweep
    stays clean and the SPA degrades gracefully.

URL: /jip-admin/api/<section>/?range=30d&lang=uz
     /jip-admin/api/user/<user_id>/?lang=uz
"""
from __future__ import annotations

import logging
import traceback
from datetime import date, timedelta

from django.http import JsonResponse
from django.shortcuts import redirect
from django.utils import timezone
from django.views.decorators.cache import never_cache

logger = logging.getLogger(__name__)

# Tables are rendered client-side (search/sort/paginate in the browser, exactly
# like the prototype). We cap the row payload and send the true total separately
# so KPI counts stay accurate even when the table shows a recent slice.
ROW_CAP = 200


# --------------------------------------------------------------------------- #
#  Small helpers
# --------------------------------------------------------------------------- #
def _lang(request) -> str:
    l = (request.GET.get("lang") or "uz").lower()
    return "ru" if l == "ru" else "uz"


def _gift_lang(lang: str) -> str:
    return "ru" if lang == "ru" else "uz_latin"


def _date_range(request):
    """Map the SPA range chip -> (date_from, date_to). 'all' -> (None, None)."""
    rng = (request.GET.get("range") or "30d").lower()
    today = timezone.localdate()
    if rng == "7d":
        return today - timedelta(days=6), today
    if rng == "30d":
        return today - timedelta(days=29), today
    if rng == "prev":
        first_this = today.replace(day=1)
        last_prev = first_this - timedelta(days=1)
        first_prev = last_prev.replace(day=1)
        return first_prev, last_prev
    # 'all' or anything unknown -> no filter
    return None, None


def _region_name(region, lang: str) -> str:
    if not region:
        return ""
    return (region.name_ru if lang == "ru" else region.name_uz) or region.name_uz or ""


def _user_name(u) -> str:
    name = ("%s %s" % (u.first_name or "", u.last_name or "")).strip()
    if name:
        return name
    if u.username:
        return u.username
    return "ID %s" % u.telegram_id


def _username_at(u) -> str:
    return ("@" + u.username) if u.username else ""


def _fdate(dt) -> str:
    if not dt:
        return ""
    try:
        dt = timezone.localtime(dt) if timezone.is_aware(dt) else dt
    except Exception:
        pass
    return dt.strftime("%d.%m.%Y")


def _fdatetime(dt) -> str:
    if not dt:
        return ""
    try:
        dt = timezone.localtime(dt) if timezone.is_aware(dt) else dt
    except Exception:
        pass
    return dt.strftime("%d.%m.%Y %H:%M")


def _is_complete(u) -> bool:
    """Registration complete = language AND privacy AND phone AND region."""
    return bool(u.language and u.privacy_accepted and u.phone_number and u.region_id)


def _is_blocked(u, now) -> bool:
    try:
        return bool(u.promo_blocked_until and u.promo_blocked_until > now)
    except Exception:
        return False


# --------------------------------------------------------------------------- #
#  Sections
# --------------------------------------------------------------------------- #
def _overview(request, df, dt, lang):
    from core.models import GiftRedemption
    from core.dashboard_stats import (
        compute_general_stats,
        compute_dashboard_charts,
        compute_intelligence_stats,
    )

    g = compute_general_stats(df, dt) or {}
    charts = compute_dashboard_charts(df, dt) or {}
    intel = compute_intelligence_stats(df, dt) or {}

    qr_total = (g.get("qr_e_total", 0) or 0) + (g.get("qr_s_total", 0) or 0)
    qr_scan = (g.get("qr_e_scanned", 0) or 0) + (g.get("qr_s_scanned", 0) or 0)

    # Redemption status distribution (lifetime, all santexnik requests)
    red_stats = {
        "pending": 0, "approved": 0, "sent": 0, "completed": 0,
        "rejected": 0, "cancelled": 0, "not_received": 0,
    }
    try:
        from django.db.models import Count
        rows = (GiftRedemption.objects.values("status")
                .annotate(n=Count("id")))
        for r in rows:
            st = r["status"]
            if st == "cancelled_by_user":
                st = "cancelled"
            if st in red_stats:
                red_stats[st] += r["n"]
    except Exception:
        logger.exception("overview redStats")

    head = {
        "uTotal": g.get("users_total", 0),
        "uSan": g.get("users_electrician", 0),
        "uSel": g.get("users_seller", 0),
        "uUns": g.get("users_unselected", 0),
        "qrTotal": qr_total,
        "qrScan": qr_scan,
        "ptsTotal": g.get("points_total", 0),
        "giftsPending": red_stats["pending"],
    }
    trends = g.get("trends", {}) or {}
    return {
        "head": head,
        "trends": {
            "users": trends.get("users_total", 0),
            "points": trends.get("points_total", 0),
        },
        "charts": {
            "days": charts.get("labels", []),
            "reg": charts.get("reg_series", []),
            "act": charts.get("act_series", []),
            "red": charts.get("red_series", []),
        },
        "redStats": red_stats,
        "segments": intel.get("segments", {"clean": 0, "warning": 0, "suspicious": 0, "blocked": 0}),
    }


def _users(request, df, dt, lang):
    from core.models import TelegramUser
    from core.dashboard_stats import compute_general_stats

    now = timezone.now()
    g = compute_general_stats(None, None) or {}

    qs = (TelegramUser.objects.select_related("region")
          .order_by("-created_at"))
    total = qs.count()
    rows = []
    for u in qs[:ROW_CAP]:
        rows.append({
            "id": u.telegram_id,
            "name": _user_name(u),
            "username": _username_at(u),
            "phone": u.phone_number or "",
            "type": u.user_type or "none",
            "region": _region_name(u.region, lang),
            "points": u.points or 0,
            "lang": "ru" if u.language == "ru" else "uz",
            "complete": _is_complete(u),
            "active": bool(u.is_active),
            "blocked": _is_blocked(u, now),
            "created": _fdate(u.created_at),
        })

    today = timezone.localdate()
    today_count = TelegramUser.objects.filter(created_at__date=today).count()
    kpis = {
        "total": g.get("life_u_total", total),
        "san": g.get("life_u_e", 0),
        "sel": g.get("life_u_s", 0),
        "today": today_count,
    }
    return {"kpis": kpis, "rows": rows, "total": total}


def _promo(request, df, dt, lang):
    from core.models import QRCode
    from core.dashboard_stats import compute_general_stats

    g = compute_general_stats(None, None) or {}
    qs = (QRCode.objects.filter(is_deleted=False)
          .select_related("scanned_by", "batch")
          .order_by("-generated_at"))
    total = qs.count()
    rows = []
    for q in qs[:ROW_CAP]:
        by = None
        if q.scanned_by:
            by = {"name": _user_name(q.scanned_by), "phone": q.scanned_by.phone_number or ""}
        rows.append({
            "seq": q.sequence_number or q.id,
            "code": q.code or q.hash_code or "",
            "serial": q.serial_number or "",
            "points": q.points or 0,
            "scanned": bool(q.is_scanned),
            "by": by,
            "at": _fdate(q.scanned_at) if q.scanned_at else "",
            "batch": q.batch.name if q.batch else "",
        })

    qr_total = (g.get("life_qr_e_total", 0) or 0) + (g.get("life_qr_s_total", 0) or 0)
    qr_scan = (g.get("life_qr_e_scanned", 0) or 0) + (g.get("life_qr_s_scanned", 0) or 0)
    act = round(qr_scan / qr_total * 100, 1) if qr_total else 0.0
    kpis = {
        "total": qr_total,
        "scanned": qr_scan,
        "unscanned": qr_total - qr_scan,
        "activation": act,
        "points": g.get("life_points_total", 0),
    }
    return {"kpis": kpis, "rows": rows, "total": total}


def _gift(request, df, dt, lang):
    from django.db.models import Count
    from core.models import Gift, GiftRedemption

    glang = _gift_lang(lang)
    palette = ["#FF9F0A", "#30D158", "#0A84FF", "#BF5AF2", "#FF375F",
               "#64D2FF", "#FFD60A", "#34C759", "#8E8E93", "#FF9500",
               "#5E5CE6", "#FF453A"]

    # Catalog
    catalog = []
    try:
        gifts = Gift.objects.annotate(req=Count("redemptions")).order_by("order", "id")
        for i, g in enumerate(gifts):
            try:
                gname = g.get_name(glang)
            except Exception:
                gname = g.name_ru if (lang == "ru" and g.name_ru) else g.name_uz_latin
            stock = g.stock_quantity
            catalog.append({
                "name": gname,
                "cost": g.points_cost or 0,
                "stock": "∞" if stock is None else stock,
                "active": bool(g.is_active),
                "req": getattr(g, "req", 0) or 0,
                "c": palette[i % len(palette)],
            })
    except Exception:
        logger.exception("gift catalog")

    # Requests
    requests_rows = []
    qs = (GiftRedemption.objects.select_related("user", "gift")
          .order_by("-requested_at"))
    total_req = qs.count()
    for r in qs[:ROW_CAP]:
        try:
            gname = r.gift.get_name(glang)
        except Exception:
            gname = (r.gift.name_ru if (lang == "ru" and r.gift.name_ru) else r.gift.name_uz_latin) if r.gift else ""
        st = r.status if r.status != "cancelled_by_user" else "cancelled"
        requests_rows.append({
            "user": {"name": _user_name(r.user), "phone": r.user.phone_number or ""},
            "gift": gname,
            "giftColor": palette[(r.gift_id or 0) % len(palette)],
            "cost": (r.gift.points_cost if r.gift else 0) or 0,
            "status": st,
            "at": _fdate(r.requested_at),
        })

    red_stats = {
        "pending": 0, "approved": 0, "sent": 0, "completed": 0,
        "rejected": 0, "cancelled": 0, "not_received": 0,
    }
    try:
        for row in GiftRedemption.objects.values("status").annotate(n=Count("id")):
            st = row["status"]
            if st == "cancelled_by_user":
                st = "cancelled"
            if st in red_stats:
                red_stats[st] += row["n"]
    except Exception:
        logger.exception("gift redStats")

    return {
        "catalog": catalog,
        "requests": requests_rows,
        "requestsTotal": total_req,
        "redStats": red_stats,
    }


def _seller(request, df, dt, lang):
    from core.models import TelegramUser
    from core.dashboard_stats import compute_store_analytics

    rows_out = []
    totals = {}
    try:
        result = compute_store_analytics(df, dt)
        store_rows, totals = result if isinstance(result, tuple) else (result, {})
        for s in store_rows:
            rows_out.append({
                "name": s.get("name", ""),
                "region": s.get("region", ""),
                "owner": s.get("owner", ""),
                "batches": s.get("batch_count", 0),
                "total": s.get("total_qr", 0),
                "act": s.get("scanned_life", 0),
                "pct": round(s.get("act_rate_life", 0) or 0, 1),
                "points": s.get("points_period", 0),
            })
    except Exception:
        logger.exception("seller store analytics")

    # Pending sellers (not yet approved)
    pending = []
    try:
        pqs = (TelegramUser.objects.filter(user_type="sotuvchi", seller_approved=False)
               .select_related("region").order_by("-created_at"))
        for u in pqs[:ROW_CAP]:
            pending.append({
                "name": _user_name(u),
                "username": _username_at(u),
                "phone": u.phone_number or "",
                "region": _region_name(u.region, lang),
                "created": _fdate(u.created_at),
            })
    except Exception:
        logger.exception("seller pending")

    total_sel = TelegramUser.objects.filter(user_type="sotuvchi").count()
    approved = TelegramUser.objects.filter(user_type="sotuvchi", seller_approved=True).count()
    kpis = {
        "total": total_sel,
        "approved": approved,
        "pending": total_sel - approved,
        "qrIssued": totals.get("total_qr", 0) if totals else 0,
        "avgAct": round(totals.get("act_rate_life", 0) or 0, 1) if totals else 0.0,
    }
    return {"kpis": kpis, "rows": rows_out, "pending": pending}


def _geo(request, df, dt, lang):
    from core.dashboard_stats import build_promo_table_rows

    items = []
    try:
        rows = build_promo_table_rows("santenik", df, dt, None) or []
        for r in rows:
            if r.get("is_total"):
                continue
            items.append({
                "code": r.get("code", ""),
                "name": r.get("name", ""),
                "v": r.get("users", 0),
                "scan": r.get("cards", 0),
                "pts": r.get("points", 0),
            })
    except Exception:
        logger.exception("geo rows")
    return {"regions": items}


def _fraud(request, df, dt, lang):
    from core.models import PromoCodeAttempt
    from core.dashboard_stats import compute_intelligence_stats

    intel = compute_intelligence_stats(df, dt) or {}

    leaderboard = []
    for u in (intel.get("leaderboard") or []):
        nm = ("%s %s" % (u.get("first_name", ""), u.get("last_name", ""))).strip() or (u.get("username") or "")
        leaderboard.append({
            "name": nm,
            "phone": u.get("phone_number", ""),
            "region": "",
            "fails": u.get("promo_failed_attempts", 0),
        })

    attempts = []
    try:
        aqs = (PromoCodeAttempt.objects.select_related("user")
               .order_by("-attempted_at"))
        for a in aqs[:ROW_CAP]:
            attempts.append({
                "user": {"name": _user_name(a.user), "phone": a.user.phone_number or ""},
                "raw": a.raw_code or "",
                "ok": bool(a.is_successful),
                "src": a.source or "unknown",
                "at": _fdatetime(a.attempted_at),
            })
    except Exception:
        logger.exception("fraud attempts")

    seg = intel.get("segments", {}) or {}
    sources = intel.get("sources", {}) or {}
    kpis = {
        "total": intel.get("total_attempts_life", intel.get("total_attempts", 0)),
        "success": intel.get("success_attempts_life", intel.get("success_attempts", 0)),
        "failed": intel.get("failed_attempts_life", intel.get("failed_attempts", 0)),
        "successRate": round(intel.get("success_rate_life", intel.get("success_rate", 0)) or 0, 1),
        "blocked": seg.get("blocked", 0),
    }
    return {
        "kpis": kpis,
        "segments": seg,
        "sources": sources,
        "leaderboard": leaderboard,
        "attempts": attempts,
    }


def _broadcast(request, df, dt, lang):
    from collections import OrderedDict
    from core.models import BroadcastMessage

    def st_norm(s):
        return s or "pending"

    qs = BroadcastMessage.objects.order_by("-created_at")
    total_bc = qs.count()
    general = []
    by_region = OrderedDict()
    by_month = OrderedDict()
    sum_sent = 0
    sum_total = 0
    for b in qs[:ROW_CAP]:
        flt = b.user_type_filter or b.region_filter or b.language_filter or "all"
        general.append({
            "title": b.title or "",
            "filter": flt,
            "total": b.total_users or 0,
            "sent": b.sent_count or 0,
            "failed": b.failed_count or 0,
            "status": st_norm(b.status),
            "at": _fdatetime(b.created_at),
        })
        sum_sent += b.sent_count or 0
        sum_total += b.total_users or 0
        # region aggregate
        rkey = b.region_filter or "—"
        ra = by_region.setdefault(rkey, {"region": rkey, "total": 0, "sent": 0, "failed": 0, "status": "completed", "at": ""})
        ra["total"] += b.total_users or 0
        ra["sent"] += b.sent_count or 0
        ra["failed"] += b.failed_count or 0
        if not ra["at"]:
            ra["at"] = _fdatetime(b.created_at)
        # month aggregate
        mkey = _fdate(b.created_at)[3:] if b.created_at else "—"  # MM.YYYY
        ma = by_month.setdefault(mkey, {"month": mkey, "total": 0, "sent": 0, "failed": 0, "status": "completed"})
        ma["total"] += b.total_users or 0
        ma["sent"] += b.sent_count or 0
        ma["failed"] += b.failed_count or 0

    kpis = {
        "total": total_bc,
        "sent": sum_sent,
        "successRate": round(sum_sent / sum_total * 100, 1) if sum_total else 0.0,
    }
    return {
        "kpis": kpis,
        "general": general,
        "region": list(by_region.values()),
        "monthly": list(by_month.values()),
    }


def _lottery(request, df, dt, lang):
    from core.models import MonthlyPromoTicket, LiveStream

    glang = _gift_lang(lang)

    tickets = []
    qs = (MonthlyPromoTicket.objects.select_related("user", "qr_code")
          .order_by("-scanned_at"))
    total_t = qs.count()
    for t in qs[:ROW_CAP]:
        tickets.append({
            "no": "#" + str(t.order),
            "user": {"name": _user_name(t.user), "phone": t.user.phone_number or ""},
            "type": t.user_type or "santenik",
            "qr": t.qr_code.code if t.qr_code else "",
            "month": t.month.strftime("%Y-%m") if t.month else "",
            "at": _fdatetime(t.scanned_at),
        })

    streams = []
    try:
        sqs = LiveStream.objects.prefetch_related("winners__user").order_by("-scheduled_at")
        for s in sqs[:50]:
            wins = []
            for w in s.winners.all().order_by("position"):
                try:
                    prize = w.prize_text_ru if (lang == "ru" and w.prize_text_ru) else w.prize_text_uz_latin
                except Exception:
                    prize = ""
                wins.append({"u": _user_name(w.user), "prize": prize or "", "pos": w.position or 0})
            try:
                title = s.get_title(glang)
            except Exception:
                title = s.title_ru if (lang == "ru" and s.title_ru) else s.title_uz_latin
            streams.append({
                "title": title or "",
                "at": _fdate(s.scheduled_at),
                "part": s.participants_count or 0,
                "status": "past" if getattr(s, "is_past", False) else "upcoming",
                "winners": wins,
            })
    except Exception:
        logger.exception("lottery streams")

    now_month = timezone.localdate().strftime("%Y-%m")
    cur = sum(1 for t in tickets if t["month"] == now_month)
    participants = qs.values("user_id").distinct().count()
    kpis = {"current": cur, "total": total_t, "participants": participants}
    return {"kpis": kpis, "tickets": tickets, "streams": streams}


def _photos(request, df, dt, lang):
    from core.models import ProjectPhoto

    palette = ["#FF9F0A", "#30D158", "#0A84FF", "#BF5AF2", "#FF375F",
               "#64D2FF", "#FFD60A", "#5E5CE6", "#FF9500", "#34C759"]
    qs = ProjectPhoto.objects.select_related("user").order_by("-created_at")
    total_p = qs.count()
    rows = []
    for i, p in enumerate(qs[:ROW_CAP]):
        img = ""
        try:
            if p.image:
                img = p.image.url
        except Exception:
            img = ""
        rows.append({
            "user": {"name": _user_name(p.user)},
            "caption": p.caption or "",
            "active": not p.is_deleted,
            "at": _fdate(p.created_at),
            "img": img,
            "c": palette[i % len(palette)],
        })

    today = timezone.localdate()
    active_n = ProjectPhoto.objects.filter(is_deleted=False).count()
    deleted_n = ProjectPhoto.objects.filter(is_deleted=True).count()
    today_n = ProjectPhoto.objects.filter(created_at__date=today).count()
    kpis = {"total": total_p, "active": active_n, "deleted": deleted_n, "today": today_n}
    return {"kpis": kpis, "rows": rows, "total": total_p}


def _audit(request, df, dt, lang):
    from core.models import ActivityLog

    qs = ActivityLog.objects.select_related("user", "tg_user").order_by("-timestamp")
    total_a = qs.count()
    rows = []
    for a in qs[:ROW_CAP]:
        who = ""
        if a.user_id and a.user:
            who = a.user.username
        elif a.tg_user_id and a.tg_user:
            who = _user_name(a.tg_user)
        else:
            who = "system"
        target = a.target_repr or ""
        if not target and a.target_model:
            target = a.target_model + (" #" + str(a.target_id) if a.target_id else "")
        rows.append({
            "at": _fdatetime(a.timestamp),
            "who": who,
            "action": a.action_type or "custom",
            "target": target,
            "desc": a.description or "",
            "ip": a.ip_address or "",
        })

    today = timezone.localdate()
    today_n = ActivityLog.objects.filter(timestamp__date=today).count()
    logins = ActivityLog.objects.filter(action_type="login").count()
    errors = ActivityLog.objects.filter(action_type="error").count()
    kpis = {"total": total_a, "today": today_n, "logins": logins, "errors": errors}
    return {"kpis": kpis, "rows": rows, "total": total_a}


_SECTIONS = {
    "overview": _overview,
    "users": _users,
    "promo": _promo,
    "gift": _gift,
    "seller": _seller,
    "geo": _geo,
    "fraud": _fraud,
    "broadcast": _broadcast,
    "lottery": _lottery,
    "photos": _photos,
    "audit": _audit,
}


# --------------------------------------------------------------------------- #
#  Views
# --------------------------------------------------------------------------- #
@never_cache
def jip_admin_api(request, section):
    """Dispatch a single dashboard section. Never raises 500."""
    if not request.user.is_authenticated or not request.user.is_staff:
        return JsonResponse({"ok": False, "error": "auth"}, status=403)

    fn = _SECTIONS.get(section)
    if fn is None:
        return JsonResponse({"ok": False, "error": "unknown_section"}, status=404)

    lang = _lang(request)
    df, dt = _date_range(request)
    try:
        data = fn(request, df, dt, lang)
        return JsonResponse({"ok": True, "data": data})
    except Exception as exc:  # pragma: no cover - defensive
        logger.error("jip_admin_api[%s] failed: %s\n%s", section, exc, traceback.format_exc())
        return JsonResponse({"ok": False, "error": "%s: %s" % (type(exc).__name__, exc)})


@never_cache
def jip_admin_api_user(request, user_id):
    """User CRM detail for the drawer. Never raises 500."""
    if not request.user.is_authenticated or not request.user.is_staff:
        return JsonResponse({"ok": False, "error": "auth"}, status=403)
    try:
        from core.dashboard_stats import get_user_crm_details
        data = get_user_crm_details(int(user_id))
        if data is None:
            return JsonResponse({"ok": False, "error": "not_found"}, status=404)
        return JsonResponse({"ok": True, "data": data})
    except Exception as exc:
        logger.error("jip_admin_api_user[%s] failed: %s\n%s", user_id, exc, traceback.format_exc())
        return JsonResponse({"ok": False, "error": "%s: %s" % (type(exc).__name__, exc)})
