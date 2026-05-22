"""Inline-клавиатуры выбора виловята/тумана для бота и помощник для подстановки координат.

Используется:
- В management-команде `request_user_location` (рассылка приглашения).
- В callback-хендлерах `setloc_*` бота для пошагового выбора локации.

Координаты дефолтов для тумана берутся из core.uz_districts_data.UZ_DISTRICTS_DATA
и записываются в user.latitude/longitude при подтверждении.
"""
from __future__ import annotations

from typing import Optional, Tuple

from aiogram import types

from core.regions import UZBEKISTAN_REGIONS
from core.uz_districts_data import UZ_DISTRICTS_DATA


CALLBACK_REGION_PREFIX = 'setloc_r:'
CALLBACK_DISTRICT_PREFIX = 'setloc_d:'
CALLBACK_BACK = 'setloc_back'


def _region_name(region_code: str, language: str) -> str:
    info = UZBEKISTAN_REGIONS.get(region_code) or {}
    if language == 'ru':
        return info.get('name_ru') or info.get('name_uz') or region_code
    return info.get('name_uz') or info.get('name_ru') or region_code


def _district_name(district: dict, language: str) -> str:
    if language == 'ru':
        return district.get('name_ru') or district.get('name_uz') or district.get('code', '')
    return district.get('name_uz') or district.get('name_ru') or district.get('code', '')


def build_region_keyboard(language: str = 'uz_latin') -> types.InlineKeyboardMarkup:
    """Inline-клавиатура со всеми виловятами Узбекистана. 2 кнопки в ряд."""
    rows: list[list[types.InlineKeyboardButton]] = []
    row: list[types.InlineKeyboardButton] = []
    for region_code in UZBEKISTAN_REGIONS.keys():
        # Показываем только виловяты, для которых есть туманы в датасете.
        if region_code not in UZ_DISTRICTS_DATA:
            continue
        btn = types.InlineKeyboardButton(
            text=_region_name(region_code, language),
            callback_data=f'{CALLBACK_REGION_PREFIX}{region_code}',
        )
        row.append(btn)
        if len(row) == 2:
            rows.append(row)
            row = []
    if row:
        rows.append(row)
    return types.InlineKeyboardMarkup(inline_keyboard=rows)


def build_district_keyboard(region_code: str, language: str = 'uz_latin', back_label: str = '« Back') -> types.InlineKeyboardMarkup:
    """Inline-клавиатура с туманами заданного виловята + кнопка "назад". 2 в ряд."""
    rows: list[list[types.InlineKeyboardButton]] = []
    row: list[types.InlineKeyboardButton] = []
    for d in UZ_DISTRICTS_DATA.get(region_code, []):
        btn = types.InlineKeyboardButton(
            text=_district_name(d, language),
            callback_data=f'{CALLBACK_DISTRICT_PREFIX}{region_code}:{d["code"]}',
        )
        row.append(btn)
        if len(row) == 2:
            rows.append(row)
            row = []
    if row:
        rows.append(row)
    rows.append([
        types.InlineKeyboardButton(text=back_label, callback_data=CALLBACK_BACK),
    ])
    return types.InlineKeyboardMarkup(inline_keyboard=rows)


def find_district_data(region_code: str, district_code: str) -> Optional[dict]:
    """Возвращает словарь тумана из датасета (code/name_uz/name_ru/lat/lon) или None."""
    for d in UZ_DISTRICTS_DATA.get(region_code, []):
        if d.get('code') == district_code:
            return d
    return None


def find_district_default_coords(region_code: str, district_code: str) -> Tuple[Optional[float], Optional[float]]:
    """Возвращает (lat, lon) дефолтных координат тумана или (None, None)."""
    d = find_district_data(region_code, district_code)
    if not d:
        return None, None
    return d.get('lat'), d.get('lon')
