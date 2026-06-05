"""T10: Eski seed'dan qolgan dublikat UzDistrict yozuvlarini tozalaydi.

Kanonik manba: core/uz_districts_data.py (UZ_DISTRICTS_DATA). Har bir viloyat
uchun kanonik district `code`lar to'plami olinadi. Kanonik bo'lmagan (eski
migratsiya 0048 dan qolgan) districtlar dublikat hisoblanadi:
  - ularga bog'langan FK lar (Store/TelegramUser/Seller.district) nomi mos
    keladigan kanonik districtga (yoki NULL ga) ko'chiriladi,
  - keyin district o'chiriladi.

Default — DRY-RUN (hech narsa o'chmaydi). Haqiqatan o'chirish: --confirm.
"""
from django.core.management.base import BaseCommand
from django.db import transaction

from core.models import UzRegion, UzDistrict, Store, TelegramUser, Seller
from core.uz_districts_data import UZ_DISTRICTS_DATA


def _norm(s):
    return (s or '').strip().lower().replace('ё', 'е')


class Command(BaseCommand):
    help = "Dublikat UzDistrict yozuvlarini tozalaydi (kanonik: uz_districts_data.py). Default dry-run."

    def add_arguments(self, parser):
        parser.add_argument(
            '--confirm', action='store_true',
            help="Haqiqatan o'chirish (aks holda faqat hisobot — dry-run).",
        )

    def handle(self, *args, **opts):
        confirm = opts['confirm']
        total_del = 0
        total_reassign = 0

        for region in UzRegion.objects.all().order_by('code'):
            canon = UZ_DISTRICTS_DATA.get(region.code, [])
            canon_codes = {d['code'] for d in canon}

            districts = list(UzDistrict.objects.filter(region=region))
            canon_objs = [d for d in districts if d.code in canon_codes]
            dups = [d for d in districts if d.code not in canon_codes]
            if not dups:
                continue

            # Nomi bo'yicha kanonik districtga ko'chirish uchun xarita.
            canon_by_name = {}
            for d in canon_objs:
                canon_by_name[_norm(d.name_ru)] = d
                canon_by_name[_norm(d.name_uz)] = d

            self.stdout.write(f"\n{region.code} ({region.name_ru}): {len(dups)} dublikat")
            for d in dups:
                repl = canon_by_name.get(_norm(d.name_ru)) or canon_by_name.get(_norm(d.name_uz))
                stores = Store.objects.filter(district=d)
                users = TelegramUser.objects.filter(district=d)
                sellers = Seller.objects.filter(district=d)
                cnt = stores.count() + users.count() + sellers.count()
                self.stdout.write(
                    f"  - o'chirish #{d.id} '{d.name_ru}' (code={d.code}) "
                    f"-> ko'chirish: {repl.name_ru if repl else 'NULL'}; FK ref: {cnt}"
                )
                if confirm:
                    with transaction.atomic():
                        stores.update(district=repl)
                        users.update(district=repl)
                        sellers.update(district=repl)
                        d.delete()
                total_reassign += cnt
                total_del += 1

        mode = "O'CHIRILDI" if confirm else "DRY-RUN (o'chirilmadi)"
        self.stdout.write(self.style.SUCCESS(
            f"\n{mode}: {total_del} dublikat district, {total_reassign} FK ko'chirildi"
        ))
        if not confirm:
            self.stdout.write("Haqiqatan tozalash uchun: python manage.py dedup_uz_districts --confirm")
