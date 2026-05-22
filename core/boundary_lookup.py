"""
Точка внутри локальных мультиполигонов OSM (GeoJSON), экспортированных из PBF
(boundary=administrative, admin_level=6). Сопоставление с UzDistrict по названиям.
"""
from __future__ import annotations

import json
import logging
import os
import re
import threading
from pathlib import Path
from typing import Any

from django.conf import settings

logger = logging.getLogger(__name__)

_lock = threading.Lock()
_cached: tuple[list[tuple[Any, dict[str, Any], float]], str | None] | None = None


def _geojson_path() -> str | None:
    p = (getattr(settings, 'UZ_ADMIN_BOUNDARIES_GEOJSON', None) or '').strip()
    if p and os.path.isfile(p):
        return p
    default = Path(settings.BASE_DIR) / 'osm-data' / 'uzbekistan_admin6.geojson'
    if default.is_file():
        return str(default)
    return None


def _admin_level(props: dict[str, Any]) -> int | None:
    v = props.get('admin_level')
    if v is not None:
        try:
            return int(str(v).strip())
        except ValueError:
            pass
    ot = props.get('other_tags')
    if isinstance(ot, str):
        m = re.search(r'"admin_level"=>"(\d+)"', ot)
        if m:
            try:
                return int(m.group(1))
            except ValueError:
                pass
    return None


def _is_admin_boundary(props: dict[str, Any]) -> bool:
    if str(props.get('boundary') or '').strip().lower() == 'administrative':
        return True
    ot = props.get('other_tags')
    if isinstance(ot, str) and '"boundary"=>"administrative"' in ot:
        return True
    return False


def _name_candidates(props: dict[str, Any]) -> list[str]:
    out: list[str] = []
    for key in ('name:ru', 'name:uz', 'name'):
        v = props.get(key)
        if isinstance(v, str) and v.strip():
            out.append(v.strip())
    ot = props.get('other_tags')
    if isinstance(ot, str):
        for m in re.finditer(r'"([^"]+)"=>"([^"]*)"', ot):
            k, val = m.group(1), m.group(2)
            if k.startswith('name') and val.strip():
                out.append(val.strip())
    seen: set[str] = set()
    uniq = []
    for s in out:
        k = s.lower()
        if k not in seen:
            seen.add(k)
            uniq.append(s)
    return uniq


def _load_geometries(geojson_path: str) -> list[tuple[Any, dict[str, Any], float]]:
    from shapely.geometry import shape
    from shapely import make_valid

    with open(geojson_path, encoding='utf-8') as f:
        data = json.load(f)
    feats = data.get('features') or []
    rows: list[tuple[Any, dict[str, Any], float]] = []
    for feat in feats:
        if not isinstance(feat, dict):
            continue
        props = feat.get('properties') or {}
        if not isinstance(props, dict):
            continue
        if _admin_level(props) != 6 or not _is_admin_boundary(props):
            continue
        geom_j = feat.get('geometry')
        if not geom_j:
            continue
        try:
            g = shape(geom_j)
        except Exception:
            continue
        if not g.is_valid:
            try:
                g = make_valid(g)
            except Exception:
                continue
        if g.is_empty:
            continue
        try:
            area = float(g.area)
        except Exception:
            area = float('inf')
        rows.append((g, props, area))
    return rows


def _get_rows() -> list[tuple[Any, dict[str, Any], float]]:
    global _cached
    path = _geojson_path()
    if not path:
        return []
    with _lock:
        if _cached is not None and _cached[1] == path:
            return _cached[0]
        try:
            rows = _load_geometries(path)
        except OSError as e:
            logger.warning('UZ boundaries GeoJSON unreadable %s: %s', path, e)
            rows = []
        except json.JSONDecodeError as e:
            logger.warning('UZ boundaries GeoJSON invalid JSON %s: %s', path, e)
            rows = []
        _cached = (rows, path)
        return rows


def resolve_uz_from_boundary_geojson(latitude: float, longitude: float):
    """
    Возвращает (UzRegion | None, UzDistrict | None) если точка попадает в полигон
    admin_level=6 и название из OSM сопоставимо со справочником UzDistrict.
    """
    from shapely.geometry import Point

    from core.geocoding import _name_matches_fragment
    from core.models import UzDistrict

    rows = _get_rows()
    if not rows:
        return None, None

    pt = Point(float(longitude), float(latitude))
    hits: list[tuple[float, dict[str, Any]]] = []
    for geom, props, area in rows:
        try:
            if geom.covers(pt):
                hits.append((area, props))
        except Exception:
            continue

    if not hits:
        return None, None

    hits.sort(key=lambda x: x[0])

    districts = list(UzDistrict.objects.select_related('region').all())
    for _, props in hits:
        for cand in _name_candidates(props):
            for d in districts:
                if _name_matches_fragment(cand, d.name_ru, d.name_uz):
                    return d.region, d

    return None, None


def clear_boundary_cache() -> None:
    """Для тестов или после замены файла GeoJSON."""
    global _cached
    with _lock:
        _cached = None
