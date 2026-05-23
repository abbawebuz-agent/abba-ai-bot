from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0070_sellerregistrationcode'),
    ]

    operations = [
        migrations.AddField(
            model_name='qrcodebatch',
            name='seller',
            field=models.ForeignKey(
                blank=True,
                limit_choices_to={'user_type': 'sotuvchi'},
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='seller_batches',
                to='core.telegramuser',
                verbose_name='Sotuvchi',
            ),
        ),
    ]
