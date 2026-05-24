from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    """Add `seller` FK to HistoricalQRCodeBatch.

    Migration 0071 added `seller` to QRCodeBatch but missed the historical
    table created by django-simple-history. Without this column, history
    INSERT after every batch save fails with 500.
    """

    dependencies = [
        ('core', '0071_qrcodebatch_seller'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalqrcodebatch',
            name='seller',
            field=models.ForeignKey(
                blank=True,
                db_constraint=False,
                limit_choices_to={'user_type': 'sotuvchi'},
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name='+',
                to='core.telegramuser',
                verbose_name='Sotuvchi',
            ),
        ),
    ]
