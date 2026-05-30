from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0075_activitylog'),
    ]

    operations = [
        migrations.AddField(
            model_name='qrcode',
            name='sequence_number',
            field=models.PositiveIntegerField(blank=True, db_index=True, null=True, unique=True, verbose_name='Tartib raqami (global)'),
        ),
        migrations.CreateModel(
            name='Seller',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name="Ism / Do'kon nomi")),
                ('phone', models.CharField(max_length=20, verbose_name='Telefon raqami')),
                ('address_other', models.CharField(blank=True, max_length=200, verbose_name='Boshqa manzil (Boshqa)')),
                ('notes', models.TextField(blank=True, verbose_name='Izoh')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name="Qo'shilgan sana")),
                ('region', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sellers', to='core.uzregion', verbose_name='Viloyat')),
                ('district', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sellers', to='core.uzdistrict', verbose_name='Tuman')),
            ],
            options={
                'verbose_name': 'Sotuvchi',
                'verbose_name_plural': 'Sotuvchilar',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='SellerBatch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('promo_from', models.PositiveIntegerField(verbose_name='Promokod dan (raqam)')),
                ('promo_to', models.PositiveIntegerField(verbose_name='Promokod gacha (raqam)')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Yaratilgan')),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seller_batches', to='core.seller', verbose_name='Sotuvchi')),
            ],
            options={
                'verbose_name': 'Sotuvchi partiyasi',
                'verbose_name_plural': 'Sotuvchi partiyalari',
                'ordering': ['-created_at'],
            },
        ),
    ]
