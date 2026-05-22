# Справочники вилоят/туман, ForeignKey у TelegramUser, перенос данных из CharField.

import django.db.models.deletion
from django.db import migrations, models


def seed_uz_geo(apps, schema_editor):
    from core.regions import UZBEKISTAN_DISTRICTS, UZBEKISTAN_REGIONS

    UzRegion = apps.get_model('core', 'UzRegion')
    UzDistrict = apps.get_model('core', 'UzDistrict')
    for code, data in UZBEKISTAN_REGIONS.items():
        UzRegion.objects.create(
            code=code,
            name_uz=data['name_uz'],
            name_ru=data['name_ru'],
        )
    for reg_code, districts in UZBEKISTAN_DISTRICTS.items():
        reg = UzRegion.objects.get(code=reg_code)
        for dcode, ddata in districts.items():
            UzDistrict.objects.create(
                region=reg,
                code=dcode,
                name_uz=ddata['name_uz'],
                name_ru=ddata['name_ru'],
            )


def migrate_telegramuser_geo_fk(apps, schema_editor):
    TelegramUser = apps.get_model('core', 'TelegramUser')
    UzRegion = apps.get_model('core', 'UzRegion')
    UzDistrict = apps.get_model('core', 'UzDistrict')
    for u in TelegramUser.objects.all().iterator(chunk_size=500):
        gr_id = gd_id = None
        rc = u.region
        dc = u.district
        if rc:
            r = UzRegion.objects.filter(code=rc).first()
            if r:
                gr_id = r.pk
                if dc:
                    d = UzDistrict.objects.filter(region_id=r.pk, code=dc).first()
                    if d:
                        gd_id = d.pk
        TelegramUser.objects.filter(pk=u.pk).update(
            geo_region_id=gr_id,
            geo_district_id=gd_id,
        )


def migrate_historical_geo_fk(apps, schema_editor):
    Hist = apps.get_model('core', 'HistoricalTelegramUser')
    UzRegion = apps.get_model('core', 'UzRegion')
    UzDistrict = apps.get_model('core', 'UzDistrict')
    for h in Hist.objects.all().iterator(chunk_size=500):
        if not h.region and not h.district:
            continue
        gr_id = gd_id = None
        if h.region:
            r = UzRegion.objects.filter(code=h.region).first()
            if r:
                gr_id = r.pk
                if h.district:
                    d = UzDistrict.objects.filter(region_id=r.pk, code=h.district).first()
                    if d:
                        gd_id = d.pk
        Hist.objects.filter(history_id=h.history_id).update(
            geo_region_id=gr_id,
            geo_district_id=gd_id,
        )


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0047_alter_historicaladmincontactsettings_history_change_reason_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='UzRegion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(db_index=True, max_length=50, unique=True)),
                ('name_uz', models.CharField(max_length=120)),
                ('name_ru', models.CharField(max_length=120)),
            ],
            options={
                'verbose_name': 'Viloyat',
                'verbose_name_plural': 'Viloyatlar',
                'ordering': ['code'],
            },
        ),
        migrations.CreateModel(
            name='UzDistrict',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(db_index=True, max_length=100)),
                ('name_uz', models.CharField(max_length=120)),
                ('name_ru', models.CharField(max_length=120)),
                (
                    'region',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='districts',
                        to='core.uzregion',
                    ),
                ),
            ],
            options={
                'verbose_name': 'Tuman',
                'verbose_name_plural': 'Tumanlar',
                'ordering': ['region__code', 'code'],
            },
        ),
        migrations.AddConstraint(
            model_name='uzdistrict',
            constraint=models.UniqueConstraint(fields=('region', 'code'), name='uniq_district_per_region'),
        ),
        migrations.RunPython(seed_uz_geo, migrations.RunPython.noop),
        migrations.AddField(
            model_name='telegramuser',
            name='geo_region',
            field=models.ForeignKey(
                blank=True,
                db_index=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='telegram_users',
                to='core.uzregion',
                verbose_name='Viloyat',
            ),
        ),
        migrations.AddField(
            model_name='telegramuser',
            name='geo_district',
            field=models.ForeignKey(
                blank=True,
                db_index=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='+',
                to='core.uzdistrict',
                verbose_name='Tuman',
            ),
        ),
        migrations.AddField(
            model_name='historicaltelegramuser',
            name='geo_region',
            field=models.ForeignKey(
                blank=True,
                db_constraint=False,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name='+',
                to='core.uzregion',
                verbose_name='Viloyat',
            ),
        ),
        migrations.AddField(
            model_name='historicaltelegramuser',
            name='geo_district',
            field=models.ForeignKey(
                blank=True,
                db_constraint=False,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name='+',
                to='core.uzdistrict',
                verbose_name='Tuman',
            ),
        ),
        migrations.RunPython(migrate_telegramuser_geo_fk, migrations.RunPython.noop),
        migrations.RunPython(migrate_historical_geo_fk, migrations.RunPython.noop),
        migrations.RemoveField(model_name='telegramuser', name='region'),
        migrations.RemoveField(model_name='telegramuser', name='district'),
        migrations.RemoveField(model_name='historicaltelegramuser', name='region'),
        migrations.RemoveField(model_name='historicaltelegramuser', name='district'),
        migrations.RenameField(model_name='telegramuser', old_name='geo_region', new_name='region'),
        migrations.RenameField(model_name='telegramuser', old_name='geo_district', new_name='district'),
        migrations.RenameField(model_name='historicaltelegramuser', old_name='geo_region', new_name='region'),
        migrations.RenameField(model_name='historicaltelegramuser', old_name='geo_district', new_name='district'),
        migrations.AlterModelOptions(
            name='telegramuser',
            options={
                'ordering': ['region__code', 'district__code', '-created_at'],
                'permissions': [
                    ('send_region_messages', 'Can send messages to users by region'),
                    ('change_user_type_call_center', 'Call Center: Can change user type'),
                ],
                'verbose_name': 'Telegram foydalanuvchisi',
                'verbose_name_plural': 'Telegram foydalanuvchilari',
            },
        ),
    ]
