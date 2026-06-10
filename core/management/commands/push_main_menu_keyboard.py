"""
Принудительно "обновляет" reply keyboard у пользователей.

Почему нужно:
- Telegram сохраняет ReplyKeyboardMarkup в чате.
- Если вы добавили новую кнопку, она появится у пользователя только после следующего сообщения
  от бота с обновлённым reply_markup (например, /start или показ главного меню).

Команда отправляет всем активным пользователям сообщение с актуальной клавиатурой.
"""

from __future__ import annotations

import asyncio

from django.conf import settings
from django.core.management.base import BaseCommand

from aiogram import Bot, types

from core.models import TelegramUser
from bot.translations import TRANSLATIONS


def _format_points(value: int | None) -> str:
    try:
        v = int(value or 0)
    except Exception:
        v = 0
    # 12 345 вместо 12,345
    return f"{v:,}".replace(",", " ")


def _t(lang: str | None, key: str) -> str:
    language = (lang or "uz_latin").strip() or "uz_latin"
    if language not in TRANSLATIONS:
        language = "uz_latin"
    return TRANSLATIONS[language].get(key) or TRANSLATIONS["uz_latin"].get(key) or key


def _build_main_menu_keyboard(lang: str | None) -> types.ReplyKeyboardMarkup:
    return types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text=_t(lang, "GIFTS"))],
            [
                types.KeyboardButton(text=_t(lang, "MY_BALANCE")),
                types.KeyboardButton(text=_t(lang, "TOP_LEADERS")),
            ],
            [types.KeyboardButton(text=_t(lang, "ENTER_PROMO_CODE"))],
            [types.KeyboardButton(text=_t(lang, "LANGUAGE"))],
            [types.KeyboardButton(text=_t(lang, "SELLER_CONTACT_ADMIN"))],
        ],
        resize_keyboard=True,
    )


class Command(BaseCommand):
    help = "Отправляет всем активным пользователям сообщение с обновлённой reply-клавиатурой главного меню"

    def add_arguments(self, parser):
        parser.add_argument(
            "--limit",
            type=int,
            default=0,
            help="Ограничить количество пользователей (0 = без ограничений)",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Не отправлять сообщения, только показать сколько было бы отправлено",
        )

    def handle(self, *args, **options):
        if not settings.TELEGRAM_BOT_TOKEN:
            self.stdout.write(self.style.ERROR("TELEGRAM_BOT_TOKEN не установлен!"))
            return

        limit = int(options.get("limit") or 0)
        dry_run = bool(options.get("dry_run"))

        qs = TelegramUser.objects.filter(is_active=True).order_by("id")
        if limit > 0:
            qs = qs[:limit]

        users = list(qs.only("id", "telegram_id", "language", "points"))
        self.stdout.write(f"Пользователей к обновлению клавиатуры: {len(users)} (dry_run={dry_run})")

        # Telegram broadcast лимит: ~30 msg/s
        delay = 1.0 / 30.0

        async def _run():
            bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
            sent = 0
            failed = 0
            try:
                for u in users:
                    if dry_run:
                        continue
                    try:
                        keyboard = _build_main_menu_keyboard(u.language)
                        text = _t(u.language, "MAIN_MENU").format(points=_format_points(u.points))
                        await bot.send_message(chat_id=u.telegram_id, text=text, reply_markup=keyboard)
                        sent += 1
                    except Exception:
                        failed += 1
                    await asyncio.sleep(delay)
            finally:
                await bot.session.close()

            return sent, failed

        if dry_run:
            self.stdout.write(self.style.SUCCESS("dry-run: сообщения не отправлялись"))
            return

        sent, failed = asyncio.run(_run())
        self.stdout.write(self.style.SUCCESS(f"Готово. Отправлено: {sent}, ошибок: {failed}"))

