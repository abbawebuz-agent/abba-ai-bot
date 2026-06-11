from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0086_backfill_welcome_bonus'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicaltelegramuser',
            name='district_custom',
            field=models.CharField(blank=True, default='', max_length=120, verbose_name="Tuman (qo'lda kiritilgan)"),
        ),
        migrations.AddField(
            model_name='telegramuser',
            name='district_custom',
            field=models.CharField(blank=True, default='', max_length=120, verbose_name="Tuman (qo'lda kiritilgan)"),
        ),
    ]
