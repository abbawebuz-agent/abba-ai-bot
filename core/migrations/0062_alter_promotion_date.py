# Generated for making Promotion.date optional

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0061_remove_historicallivestream_cover_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promotion',
            name='date',
            field=models.DateField(blank=True, null=True, verbose_name='Sana'),
        ),
        migrations.AlterField(
            model_name='historicalpromotion',
            name='date',
            field=models.DateField(blank=True, null=True, verbose_name='Sana'),
        ),
    ]
