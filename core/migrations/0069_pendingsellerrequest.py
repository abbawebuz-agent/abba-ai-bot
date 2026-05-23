from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0068_telegramuser_seller_approved'),
    ]

    operations = [
        migrations.CreateModel(
            name='PendingSellerRequest',
            fields=[],
            options={
                'verbose_name': 'Zapros (sotuvchi arizasi)',
                'verbose_name_plural': 'Zaproslar',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('core.telegramuser',),
        ),
    ]
