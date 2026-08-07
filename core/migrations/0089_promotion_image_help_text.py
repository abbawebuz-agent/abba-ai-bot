from django.db import migrations, models

IMAGE_HELP = (
    "Tavsiya etilgan o'lcham: 1000x500 px (2:1). "
    "Boshqa nisbatdagi rasm markazi bo'yicha kesiladi."
)
URL_HELP = (
    "Tashqi rasm URL'i (tavsiya: 1000x500 px). To'ldirilsa, yuklangan fayldan ustun turadi "
    "(media saqlanmaganda ham ishlaydi)."
)


class Migration(migrations.Migration):
    """Faqat help_text yangilanishi (DB sxemasi o'zgarmaydi)."""

    dependencies = [
        ('core', '0088_sellerbatch_manual_promo_from'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promotion',
            name='image',
            field=models.ImageField(
                blank=True, null=True, upload_to='promotions/',
                help_text=IMAGE_HELP,
                verbose_name='Banner rasmi (fayl)',
            ),
        ),
        migrations.AlterField(
            model_name='historicalpromotion',
            name='image',
            field=models.TextField(
                blank=True, null=True, max_length=100,
                help_text=IMAGE_HELP,
                verbose_name='Banner rasmi (fayl)',
            ),
        ),
        migrations.AlterField(
            model_name='promotion',
            name='image_url',
            field=models.URLField(
                blank=True, default='', max_length=500,
                help_text=URL_HELP,
                verbose_name='Banner rasmi (internet havola)',
            ),
        ),
        migrations.AlterField(
            model_name='historicalpromotion',
            name='image_url',
            field=models.URLField(
                blank=True, default='', max_length=500,
                help_text=URL_HELP,
                verbose_name='Banner rasmi (internet havola)',
            ),
        ),
    ]
