"""
Keyboard factory functions.
"""
from __future__ import annotations

from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    WebAppInfo,
)

from .translations import t


def kb_language() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="🇺🇿 O'zbekcha", callback_data="lang:uz_latin"),
        InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang:ru"),
    ]])


def kb_user_type(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t(lang, 'btn_santenik'), callback_data="role:santenik")],
        [InlineKeyboardButton(text=t(lang, 'btn_sotuvchi'), callback_data="role:sotuvchi")],
    ])


def kb_privacy(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text=t(lang, 'btn_agree'), callback_data="privacy:agree"),
        InlineKeyboardButton(text=t(lang, 'btn_disagree'), callback_data="privacy:disagree"),
    ]])


def kb_phone(lang: str) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=t(lang, 'btn_share_phone'), request_contact=True)]],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def kb_location(lang: str) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=t(lang, 'btn_share_location'), request_location=True)]],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def kb_yes_no(lang: str, prefix: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text=t(lang, 'btn_yes'), callback_data=f"{prefix}:yes"),
        InlineKeyboardButton(text=t(lang, 'btn_no'), callback_data=f"{prefix}:no"),
    ]])


def kb_santenik_menu(lang: str, web_app_url: str | None = None) -> ReplyKeyboardMarkup:
    rows = [
        [KeyboardButton(text=t(lang, 'menu_balance')), KeyboardButton(text=t(lang, 'menu_gifts'))],
        [KeyboardButton(text=t(lang, 'menu_orders'))],
        [KeyboardButton(text=t(lang, 'menu_top_month')), KeyboardButton(text=t(lang, 'menu_top_all'))],
        [KeyboardButton(text=t(lang, 'menu_video')), KeyboardButton(text=t(lang, 'menu_language'))],
        [KeyboardButton(text=t(lang, 'menu_help'))],
    ]
    if web_app_url:
        rows[1].append(KeyboardButton(
            text=t(lang, 'menu_webapp'),
            web_app=WebAppInfo(url=f"{web_app_url}/webapp/"),
        ))
    return ReplyKeyboardMarkup(keyboard=rows, resize_keyboard=True)


def kb_seller_menu(lang: str, web_app_url: str | None = None) -> ReplyKeyboardMarkup:
    rows = [
        [KeyboardButton(text=t(lang, 'menu_my_balance'))],
        [KeyboardButton(text=t(lang, 'menu_sales_history'))],
        [KeyboardButton(text=t(lang, 'menu_my_store'))],
    ]
    if web_app_url:
        rows.append([KeyboardButton(
            text=t(lang, 'menu_webapp'),
            web_app=WebAppInfo(url=f"{web_app_url}/webapp/seller/"),
        )])
    rows.append([
        KeyboardButton(text=t(lang, 'menu_language')),
        KeyboardButton(text=t(lang, 'menu_admin_contact')),
    ])
    return ReplyKeyboardMarkup(keyboard=rows, resize_keyboard=True)


def kb_remove() -> ReplyKeyboardRemove:
    return ReplyKeyboardRemove()
