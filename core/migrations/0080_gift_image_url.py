from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0079_sellerbatch_promo_from_nullable'),
    ]

    operations = [
        migrations.AddField(
            model_name='gift',
            name='image_url',
            field=models.URLField(
                blank=True, default='', max_length=500,
                help_text="Tashqi rasm URL'i. To'ldirilsa, yuklangan fayldan ustun turadi.",
                verbose_name='Rasm (internet havola)',
            ),
        ),
        migrations.AddField(
            model_name='historicalgift',
            name='image_url',
            field=models.URLField(
                blank=True, default='', max_length=500,
                help_text="Tashqi rasm URL'i. To'ldirilsa, yuklangan fayldan ustun turadi.",
                verbose_name='Rasm (internet havola)',
            ),
        ),
        migrations.AlterField(
            model_name='gift',
            name='image',
            field=models.ImageField(
                blank=True, null=True, upload_to='gifts/',
                verbose_name='Rasm (fayl)',
            ),
        ),
        migrations.AlterField(
            model_name='historicalgift',
            name='image',
            field=models.TextField(
                blank=True, null=True, max_length=100,
                verbose_name='Rasm (fayl)',
            ),
        ),
    ]
