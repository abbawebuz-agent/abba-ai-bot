from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0062_alter_promotion_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='livestream',
            name='banner',
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to='live_streams/banners/',
                verbose_name='Webapp banneri',
                help_text="Webapp ichida efir kartochkasi va detal sahifasida ko'rsatiladi",
            ),
        ),
        migrations.AddField(
            model_name='livestream',
            name='participants_count',
            field=models.PositiveIntegerField(
                blank=True,
                null=True,
                verbose_name='Ishtirokchilar soni',
                help_text="Webapp'da ko'rsatiladigan ishtirokchilar soni (qo'lda kiritiladi)",
            ),
        ),
        migrations.AddField(
            model_name='historicallivestream',
            name='banner',
            field=models.TextField(
                blank=True,
                max_length=100,
                null=True,
                verbose_name='Webapp banneri',
                help_text="Webapp ichida efir kartochkasi va detal sahifasida ko'rsatiladi",
            ),
        ),
        migrations.AddField(
            model_name='historicallivestream',
            name='participants_count',
            field=models.PositiveIntegerField(
                blank=True,
                null=True,
                verbose_name='Ishtirokchilar soni',
                help_text="Webapp'da ko'rsatiladigan ishtirokchilar soni (qo'lda kiritiladi)",
            ),
        ),
    ]
