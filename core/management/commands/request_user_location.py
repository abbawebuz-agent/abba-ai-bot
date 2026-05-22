"""Management command для рассылки приглашения указать локацию (виловят/туман).

Отправляет всем пользователям, у которых отсутствует `latitude` или `longitude`,
сообщение с inline-клавиатурой выбора виловята. После выбора виловята → тумана
координаты по умолчанию (центр админ-центра тумана) записываются в профиль
пользователя.

Использование:
    python manage.py request_user_location
    python manage.py request_user_location --limit 10 --dry-run
    python manage.py request_user_location --include-inactive
"""
import asyncio

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.models import Q

from aiogram import Bot

from bot.translations import get_text
from bot.location_picker import build_region_keyboard
from core.messaging import send_message_to_user
from core.models import TelegramUser


class Command(BaseCommand):
    help = (
        "Отправляет пользователям без координат (latitude/longitude=NULL) "
        "приглашение выбрать виловят/туман через inline-клавиатуру."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--include-inactive",
            action="store_true",
            help=(
                "Включать неактивных пользователей (заблокировавших бота). "
                "Если до сих пор заблокирован — отправка упадёт с Forbidden."
            ),
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
            help="Не отправлять — только показать количество получателей",
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

        include_inactive = bool(options["include_inactive"])
        limit = int(options["limit"] or 0)
        dry_run = bool(options["dry_run"])
        delay = float(options["delay"])

        users_qs = TelegramUser.objects.filter(
            Q(latitude__isnull=True) | Q(longitude__isnull=True)
        ).order_by("id")
        if not include_inactive:
            users_qs = users_qs.filter(is_active=True)
        if limit > 0:
            users_qs = users_qs[:limit]

        total = users_qs.count()
        self.stdout.write(f"Получателей без координат: {total}")
        if dry_run or total == 0:
            return

        # Sync-предзагрузка: внутри asyncio не дёргаем ORM напрямую.
        users = list(users_qs)

        async def run():
            bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
            sent = 0
            failed = 0
            try:
                for idx, user in enumerate(users):
                    language = user.language or 'uz_latin'
                    text = get_text(user, 'LOCATION_REQUEST_PROMPT')
                    keyboard = build_region_keyboard(language)
                    ok, err = await send_message_to_user(
                        bot=bot,
                        user=user,
                        text=text,
                        reply_markup=keyboard,
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

            self.stdout.write(self.style.SUCCESS(
                f"Готово. Отправлено: {sent}, ошибок: {failed}, всего: {total}"
            ))

        asyncio.run(run())
