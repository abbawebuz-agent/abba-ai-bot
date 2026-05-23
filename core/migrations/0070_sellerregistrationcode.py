from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0069_pendingsellerrequest'),
    ]

    operations = [
        migrations.CreateModel(
            name='SellerRegistrationCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=8, unique=True, verbose_name='ID (8 raqam)')),
                ('label', models.CharField(blank=True, max_length=255, verbose_name='Izoh (ixtiyoriy)')),
                ('is_used', models.BooleanField(db_index=True, default=False, verbose_name='Ishlatilgan')),
                ('used_at', models.DateTimeField(blank=True, null=True, verbose_name='Ishlatilgan vaqt')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('used_by', models.ForeignKey(
                    blank=True, null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    related_name='seller_codes',
                    to='core.telegramuser',
                    verbose_name='Kim ishlatdi',
                )),
            ],
            options={
                'verbose_name': 'Sotuvchi ID',
                'verbose_name_plural': 'Sotuvchi IDlari',
                'ordering': ['-created_at'],
            },
        ),
    ]
