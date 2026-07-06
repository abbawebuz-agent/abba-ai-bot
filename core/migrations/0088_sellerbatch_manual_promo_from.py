from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0087_telegramuser_district_custom'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sellerbatch',
            name='promo_from',
            field=models.PositiveIntegerField(
                blank=False,
                null=True,
                help_text="Diapazon boshlanish raqami — qo'lda kiriting.",
                verbose_name='Promokod dan (raqam)',
            ),
        ),
    ]
