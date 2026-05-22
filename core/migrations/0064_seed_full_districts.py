"""Заполняет UzDistrict полным набором туманов Узбекистана.

Координаты не хранятся на модели — они нужны только для подстановки
в `TelegramUser.latitude/longitude` при выборе тумана пользователем,
и берутся напрямую из `core.uz_districts_data.UZ_DISTRICTS_DATA`.
"""

from django.db import migrations


def upsert_districts(apps, schema_editor):
    from core.uz_districts_data import UZ_DISTRICTS_DATA

    UzRegion = apps.get_model('core', 'UzRegion')
    UzDistrict = apps.get_model('core', 'UzDistrict')

    for region_code, districts in UZ_DISTRICTS_DATA.items():
        region = UzRegion.objects.filter(code=region_code).first()
        if not region:
            continue
        for d in districts:
            UzDistrict.objects.update_or_create(
                region=region,
                code=d['code'],
                defaults={
                    'name_uz': d['name_uz'],
                    'name_ru': d['name_ru'],
                },
            )


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0063_livestream_banner_participants'),
    ]

    operations = [
        migrations.RunPython(upsert_districts, migrations.RunPython.noop),
    ]
