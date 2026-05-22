"""
Management command для напоминания пользователям продолжить регистрацию.

Использует ORM (TelegramUser) для выбора пользователей с незавершённой регистрацией
и отправляет им заданный текст (например: "Продолжите регистрацию, нажмите /start").
"""

import asyncio

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.models import Q

from aiogram import Bot

from core.messaging import send_message_to_user
from core.models import TelegramUser


def _incomplete_registration_q() -> Q:
    """
    Условия "регистрация НЕ завершена" — должны совпадать с логикой бота.

    См. bot/bot.py::is_registration_complete:
      language, first_name, user_type, privacy_accepted, phone_number, latitude, longitude
    """
    return (
        Q(language__isnull=True) | Q(language="") |
        Q(first_name__isnull=True) | Q(first_name="") |
        Q(user_type__isnull=True) | Q(user_type="") |
        Q(privacy_accepted=False) |
        Q(phone_number__isnull=True) | Q(phone_number="") |
        Q(latitude__isnull=True) |
        Q(longitude__isnull=True)
    )


class Command(BaseCommand):
    help = "Отправляет напоминание о регистрации (нажмите /start) незарегистрированным пользователям"

    def add_arguments(self, parser):
        parser.add_argument(
            "--text",
            required=True,
            type=str,
            help="Текст сообщения (поддерживает HTML при --parse-mode=HTML)",
        )
        parser.add_argument(
            "--parse-mode",
            type=str,
            choices=["HTML", "Markdown"],
            default="HTML",
            help="Режим парсинга текста",
        )
        parser.add_argument(
            "--include-inactive",
            action="store_true",
            help="Включать неактивных пользователей (в т.ч. ранее заблокировавших бота). "
                 "Если пользователь всё ещё заблокировал — отправка упадёт с Forbidden и он останется is_active=False.",
        )
        parser.add_argument(
            "--limit",
            type=int,
            default=0,
            help="Ограничить количество получателей (0 = без лимита)",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Не отправлять сообщения, только вывести количество получателей",
        )
        parser.add_argument(
            "--delay",
            type=float,
            default=1.0 / 30.0,
            help="Задержка между сообщениями (сек), по умолчанию ~0.033 (30 msg/s)",
        )

    def handle(self, *args, **options):
        if not settings.TELEGRAM_BOT_TOKEN:
            self.stdout.write(self.style.ERROR("TELEGRAM_BOT_TOKEN не установлен!"))
            return

        text = options["text"]
        parse_mode = options["parse_mode"]
        include_inactive = options["include_inactive"]
        limit = int(options["limit"] or 0)
        dry_run = bool(options["dry_run"])
        delay = float(options["delay"])

        users_qs = TelegramUser.objects.filter(_incomplete_registration_q()).order_by("id")
        if not include_inactive:
            users_qs = users_qs.filter(is_active=True)
        if limit > 0:
            users_qs = users_qs[:limit]

        total = users_qs.count()
        self.stdout.write(f"Получателей: {total}")
        if dry_run or total == 0:
            return

        # ВАЖНО: Django ORM нельзя трогать внутри asyncio-loop без sync_to_async.
        # Поэтому забираем пользователей заранее (в sync-контексте), а в async оставляем только Telegram API.
        users = list(users_qs)

        async def run():
            bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
            sent = 0
            failed = 0
            try:
                for idx, user in enumerate(users):
                    ok, err = await send_message_to_user(
                        bot=bot,
                        user=user,
                        text=text,
                        parse_mode=parse_mode,
                        disable_link_preview=True,
                    )
                    if ok:
                        sent += 1
                    else:
                        failed += 1
                        self.stderr.write(f"[{user.telegram_id}] failed: {err}")

                    if idx < len(users) - 1 and delay > 0:
                        await asyncio.sleep(delay)
            finally:
                await bot.session.close()

            self.stdout.write(self.style.SUCCESS(f"Готово. Отправлено: {sent}, ошибок: {failed}, всего: {total}"))

        asyncio.run(run())

