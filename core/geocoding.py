"""
Обратное геокодирование через локальный Nominatim (OSM) и сопоставление со справочниками UzRegion/UzDistrict.
"""
from __future__ import annotations

import json
import re
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

from django.conf import settings


def _normalize(s: str) -> str:
    s = s.lower().strip()
    s = s.replace('ʻ', "'").replace('’', "'").replace('`', "'")
    s = re.sub(r'\s+', ' ', s)
    return s


def _name_matches_fragment(frag: str, name_ru: str, name_uz: str) -> bool:
    if not frag:
        return False
    f = _normalize(frag)
    if len(f) < 2:
        return False
    for n in (name_ru, name_uz):
        t = _normalize(n)
        if not t:
            continue
        if f == t or f in t or t in f:
            return True
    return False


def reverse_geocode_osm(latitude: float, longitude: float) -> dict[str, Any] | None:
    """GET /reverse Nominatim. Без NOMINATIM_BASE_URL возвращает None."""
    base = getattr(settings, 'NOMINATIM_BASE_URL', '') or ''
    base = base.strip().rstrip('/')
    if not base:
        return None

    params = urllib.parse.urlencode(
        {
            'lat': latitude,
            'lon': longitude,
            'format': 'json',
            'addressdetails': 1,
            'zoom': 18,
            'accept-language': 'ru,uz,en',
        }
    )
    url = f'{base}/reverse?{params}'
    req = urllib.request.Request(
        url,
        headers={'User-Agent': getattr(settings, 'NOMINATIM_USER_AGENT', 'mona-bot/1.0 (local nominatim)')},
    )
    try:
        with urllib.request.urlopen(req, timeout=getattr(settings, 'NOMINATIM_TIMEOUT', 10)) as resp:
            raw = resp.read().decode()
    except (urllib.error.URLError, TimeoutError, OSError):
        return None
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return None


def _address_fragments(address: dict[str, Any]) -> list[str]:
    keys = (
        'state',
        'region',
        'county',
        'state_district',
        'city',
        'town',
        'village',
        'municipality',
        'suburb',
        'city_district',
        'district',
        'neighbourhood',
        'hamlet',
    )
    out: list[str] = []
    for k in keys:
        v = address.get(k)
        if isinstance(v, str) and v.strip():
            out.append(v.strip())
    return out


def resolve_uz_region_district(latitude: float, longitude: float):
    """
    Возвращает (UzRegion | None, UzDistrict | None) по ответу Nominatim и справочнику в БД.
    Если Nominatim недоступен или не сматчился — (None, None).
    """
    from core.models import UzDistrict, UzRegion

    payload = reverse_geocode_osm(latitude, longitude)
    if not payload:
        return None, None

    addr = payload.get('address')
    if not isinstance(addr, dict):
        return None, None

    fragments = _address_fragments(addr)
    if not fragments:
        return None, None

    regions = list(UzRegion.objects.all())
    matched_region = None
    for frag in fragments:
        for r in regions:
            if _name_matches_fragment(frag, r.name_ru, r.name_uz):
                matched_region = r
                break
        if matched_region:
            break

    if matched_region is None:
        return None, None

    districts = list(
        UzDistrict.objects.filter(region=matched_region).select_related('region')
    )
    matched_district = None
    for frag in fragments:
        for d in districts:
            if _name_matches_fragment(frag, d.name_ru, d.name_uz):
                matched_district = d
                break
        if matched_district:
            break

    return matched_region, matched_district
