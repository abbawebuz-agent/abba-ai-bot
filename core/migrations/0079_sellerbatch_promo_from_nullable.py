"""SellerBatch.promo_from endi avtomatik to'ldiriladi (max+1).

Foydalanuvchi qo'lda kirita olmaydi — null=True, blank=True qilamiz,
save() avtomatik tuldiradi.
"""
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0078_fix_historicalqrcode_sequence'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sellerbatch',
            name='promo_from',
            field=models.PositiveIntegerField(
                blank=True,
                null=True,
                help_text="Avtomatik (oxirgi partiya + 1) — saqlanganda o'zgartirilmaydi.",
                verbose_name='Promokod dan (raqam)',
            ),
        ),
    ]
