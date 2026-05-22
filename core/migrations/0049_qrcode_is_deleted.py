# Soft-delete flag for QR codes

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0048_uz_geo_and_telegramuser_fk'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalqrcode',
            name='is_deleted',
            field=models.BooleanField(db_index=True, default=False, verbose_name='Oʻchirilgan (yumshoq)'),
        ),
        migrations.AddField(
            model_name='qrcode',
            name='is_deleted',
            field=models.BooleanField(db_index=True, default=False, verbose_name='Oʻchirilgan (yumshoq)'),
        ),
    ]
