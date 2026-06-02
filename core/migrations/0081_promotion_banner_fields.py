from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0080_gift_image_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='promotion',
            name='image_url',
            field=models.URLField(
                blank=True, default='', max_length=500,
                help_text="Tashqi rasm URL'i. To'ldirilsa, yuklangan fayldan ustun turadi.",
                verbose_name='Banner rasmi (internet havola)',
            ),
        ),
        migrations.AddField(
            model_name='promotion',
            name='link_url',
            field=models.URLField(
                blank=True, default='', max_length=500,
                help_text='Banner bosilganda ochiladigan URL (ixtiyoriy).',
                verbose_name='Havola (bosilganda)',
            ),
        ),
        migrations.AddField(
            model_name='historicalpromotion',
            name='image_url',
            field=models.URLField(
                blank=True, default='', max_length=500,
                help_text="Tashqi rasm URL'i. To'ldirilsa, yuklangan fayldan ustun turadi.",
                verbose_name='Banner rasmi (internet havola)',
            ),
        ),
        migrations.AddField(
            model_name='historicalpromotion',
            name='link_url',
            field=models.URLField(
                blank=True, default='', max_length=500,
                help_text='Banner bosilganda ochiladigan URL (ixtiyoriy).',
                verbose_name='Havola (bosilganda)',
            ),
        ),
        migrations.AlterField(
            model_name='promotion',
            name='image',
            field=models.ImageField(
                blank=True, null=True, upload_to='promotions/',
                verbose_name='Banner rasmi (fayl)',
            ),
        ),
        migrations.AlterField(
            model_name='historicalpromotion',
            name='image',
            field=models.TextField(
                blank=True, null=True, max_length=100,
                verbose_name='Banner rasmi (fayl)',
            ),
        ),
    ]
