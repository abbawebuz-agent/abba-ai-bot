from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0067_remove_smartupid_qrcodegeneration'),
    ]

    operations = [
        migrations.AddField(
            model_name='telegramuser',
            name='seller_approved',
            field=models.BooleanField(
                db_index=True,
                default=False,
                help_text='Faqat sotuvchilar uchun. Admin tasdiqlagunicha False.',
                verbose_name='Sotuvchi tasdiqlangan',
            ),
        ),
        migrations.AddField(
            model_name='telegramuser',
            name='seller_approved_at',
            field=models.DateTimeField(
                blank=True,
                null=True,
                verbose_name='Tasdiqlangan vaqt',
            ),
        ),
        migrations.AddField(
            model_name='historicaltelegramuser',
            name='seller_approved',
            field=models.BooleanField(
                db_index=True,
                default=False,
                help_text='Faqat sotuvchilar uchun. Admin tasdiqlagunicha False.',
                verbose_name='Sotuvchi tasdiqlangan',
            ),
        ),
        migrations.AddField(
            model_name='historicaltelegramuser',
            name='seller_approved_at',
            field=models.DateTimeField(
                blank=True,
                null=True,
                verbose_name='Tasdiqlangan vaqt',
            ),
        ),
    ]
