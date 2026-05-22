"""JIP transformation migration:
- TelegramUser.USER_TYPE_CHOICES: electrician->santenik, seller->sotuvchi
- TelegramUser.smartup_id field deleted
- New models: Store, QRCodeBatch, SellerPointsTransaction
- QRCode: + store FK, + batch FK, - code_type field
- Gift: - user_type field, + stock_quantity
- GiftRedemption.user limited to santenik
- MonthlyPromoTicket: + store FK
- BroadcastMessage: + store_filter FK

Data migration:
- Convert all 'electrician' user_type to 'santenik'
- Convert all 'seller' user_type to 'sotuvchi'
- Convert all 'electrician' code_type QRs (drop) -> they get NULL store
- Same for gifts: user_type='electrician'/'seller' -> NULL (gift available to all)
"""
from django.db import migrations, models
import django.db.models.deletion
import django.core.validators
import simple_history.models
from django.conf import settings


def migrate_user_types(apps, schema_editor):
    """electrician → santenik, seller → sotuvchi."""
    TelegramUser = apps.get_model('core', 'TelegramUser')
    TelegramUser.objects.filter(user_type='electrician').update(user_type='santenik')
    TelegramUser.objects.filter(user_type='seller').update(user_type='sotuvchi')

    # Same in MonthlyPromoTicket
    MonthlyPromoTicket = apps.get_model('core', 'MonthlyPromoTicket')
    MonthlyPromoTicket.objects.filter(user_type='electrician').update(user_type='santenik')
    MonthlyPromoTicket.objects.filter(user_type='seller').update(user_type='sotuvchi')


def migrate_user_types_reverse(apps, schema_editor):
    TelegramUser = apps.get_model('core', 'TelegramUser')
    TelegramUser.objects.filter(user_type='santenik').update(user_type='electrician')
    TelegramUser.objects.filter(user_type='sotuvchi').update(user_type='seller')

    MonthlyPromoTicket = apps.get_model('core', 'MonthlyPromoTicket')
    MonthlyPromoTicket.objects.filter(user_type='santenik').update(user_type='electrician')
    MonthlyPromoTicket.objects.filter(user_type='sotuvchi').update(user_type='seller')


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0065_merge_global_ticket_order_seed_full_districts'),
    ]

    operations = [
        # --- Data: convert types first (must run BEFORE choices change) ---
        migrations.RunPython(migrate_user_types, migrate_user_types_reverse),

        # --- Store model ---
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, verbose_name="Do'kon nomi")),
                ('legal_name', models.CharField(blank=True, max_length=255, verbose_name='Yuridik nomi')),
                ('phone', models.CharField(max_length=20, verbose_name='Telefon')),
                ('address', models.TextField(verbose_name="To'liq manzil")),
                ('latitude', models.FloatField(blank=True, null=True)),
                ('longitude', models.FloatField(blank=True, null=True)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='stores/logos/', verbose_name='Logo')),
                ('commission_percent', models.DecimalField(decimal_places=2, default=5.00, max_digits=5, verbose_name='Komissiya foizi')),
                ('contract_signed_at', models.DateField(blank=True, null=True, verbose_name='Shartnoma sanasi')),
                ('is_active', models.BooleanField(db_index=True, default=True, verbose_name='Faol')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='stores', to='core.uzregion', verbose_name='Viloyat')),
                ('district', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='stores', to='core.uzdistrict', verbose_name='Tuman')),
                ('owner', models.ForeignKey(blank=True, limit_choices_to={'user_type': 'sotuvchi'}, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='owned_stores', to='core.telegramuser', verbose_name='Egasi (sotuvchi)')),
            ],
            options={
                'verbose_name': "Do'kon",
                'verbose_name_plural': "Do'konlar",
                'ordering': ['region__code', 'name'],
                'indexes': [models.Index(fields=['is_active', 'region'], name='core_store_is_acti_idx')],
            },
        ),

        # Historical model for Store
        migrations.CreateModel(
            name='HistoricalStore',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name="Do'kon nomi")),
                ('legal_name', models.CharField(blank=True, max_length=255, verbose_name='Yuridik nomi')),
                ('phone', models.CharField(max_length=20, verbose_name='Telefon')),
                ('address', models.TextField(verbose_name="To'liq manzil")),
                ('latitude', models.FloatField(blank=True, null=True)),
                ('longitude', models.FloatField(blank=True, null=True)),
                ('logo', models.TextField(blank=True, max_length=100, null=True, verbose_name='Logo')),
                ('commission_percent', models.DecimalField(decimal_places=2, default=5.00, max_digits=5, verbose_name='Komissiya foizi')),
                ('contract_signed_at', models.DateField(blank=True, null=True, verbose_name='Shartnoma sanasi')),
                ('is_active', models.BooleanField(db_index=True, default=True, verbose_name='Faol')),
                ('created_at', models.DateTimeField(blank=True, editable=False)),
                ('updated_at', models.DateTimeField(blank=True, editable=False)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('region', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='core.uzregion', verbose_name='Viloyat')),
                ('district', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='core.uzdistrict', verbose_name='Tuman')),
                ('owner', models.ForeignKey(blank=True, db_constraint=False, limit_choices_to={'user_type': 'sotuvchi'}, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='core.telegramuser', verbose_name='Egasi (sotuvchi)')),
            ],
            options={
                'verbose_name': "historical Do'kon",
                'verbose_name_plural': "historical Do'konlar",
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),

        # --- QRCodeBatch model ---
        migrations.CreateModel(
            name='QRCodeBatch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(help_text='Avtomatik: STORE-MAY-2026-001', max_length=100, verbose_name='Batch nomi')),
                ('quantity', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='Miqdor (kartalar soni)')),
                ('points_per_code', models.IntegerField(default=50, validators=[django.core.validators.MinValueValidator(1)], verbose_name='Har karta uchun ball')),
                ('status', models.CharField(choices=[('pending', 'Kutilmoqda'), ('processing', 'Generatsiya jarayonida'), ('completed', 'Tayyor'), ('failed', 'Xatolik')], default='pending', max_length=20, verbose_name='Holat')),
                ('zip_file', models.FileField(blank=True, null=True, upload_to='batches/', verbose_name='ZIP fayl')),
                ('error_message', models.TextField(blank=True, verbose_name='Xato xabari')),
                ('delivery_status', models.CharField(choices=[('not_shipped', "Hali jo'natilmagan"), ('shipped', "Jo'natildi"), ('delivered', 'Yetkazib berildi')], default='not_shipped', max_length=20, verbose_name='Yetkazib berish holati')),
                ('shipped_at', models.DateTimeField(blank=True, null=True)),
                ('delivered_at', models.DateTimeField(blank=True, null=True)),
                ('delivered_by', models.CharField(blank=True, max_length=255, verbose_name='Agent ismi')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('completed_at', models.DateTimeField(blank=True, null=True)),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='batches', to='core.store', verbose_name="Do'kon")),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='batches_created', to=settings.AUTH_USER_MODEL, verbose_name='Kim yaratgan')),
            ],
            options={
                'verbose_name': 'Batch',
                'verbose_name_plural': "Batch'lar",
                'ordering': ['-created_at'],
                'constraints': [models.UniqueConstraint(fields=['name', 'store'], name='uniq_batch_name_per_store')],
                'indexes': [
                    models.Index(fields=['status', '-created_at'], name='core_qrcode_status_idx'),
                    models.Index(fields=['store', 'delivery_status'], name='core_qrcode_store_d_idx'),
                ],
            },
        ),

        # Historical model for QRCodeBatch
        migrations.CreateModel(
            name='HistoricalQRCodeBatch',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('name', models.CharField(help_text='Avtomatik: STORE-MAY-2026-001', max_length=100, verbose_name='Batch nomi')),
                ('quantity', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='Miqdor (kartalar soni)')),
                ('points_per_code', models.IntegerField(default=50, validators=[django.core.validators.MinValueValidator(1)], verbose_name='Har karta uchun ball')),
                ('status', models.CharField(choices=[('pending', 'Kutilmoqda'), ('processing', 'Generatsiya jarayonida'), ('completed', 'Tayyor'), ('failed', 'Xatolik')], default='pending', max_length=20, verbose_name='Holat')),
                ('zip_file', models.TextField(blank=True, max_length=100, null=True, verbose_name='ZIP fayl')),
                ('error_message', models.TextField(blank=True, verbose_name='Xato xabari')),
                ('delivery_status', models.CharField(choices=[('not_shipped', "Hali jo'natilmagan"), ('shipped', "Jo'natildi"), ('delivered', 'Yetkazib berildi')], default='not_shipped', max_length=20, verbose_name='Yetkazib berish holati')),
                ('shipped_at', models.DateTimeField(blank=True, null=True)),
                ('delivered_at', models.DateTimeField(blank=True, null=True)),
                ('delivered_by', models.CharField(blank=True, max_length=255, verbose_name='Agent ismi')),
                ('created_at', models.DateTimeField(blank=True, editable=False)),
                ('completed_at', models.DateTimeField(blank=True, null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('store', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='core.store', verbose_name="Do'kon")),
                ('created_by', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Kim yaratgan')),
            ],
            options={
                'verbose_name': 'historical Batch',
                'verbose_name_plural': "historical Batch'lar",
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),

        # --- TelegramUser changes ---
        migrations.AlterField(
            model_name='telegramuser',
            name='user_type',
            field=models.CharField(blank=True, choices=[('santenik', 'Santenik'), ('sotuvchi', 'Sotuvchi')], max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='historicaltelegramuser',
            name='user_type',
            field=models.CharField(blank=True, choices=[('santenik', 'Santenik'), ('sotuvchi', 'Sotuvchi')], max_length=20, null=True),
        ),
        migrations.RemoveField(
            model_name='telegramuser',
            name='smartup_id',
        ),
        migrations.RemoveField(
            model_name='historicaltelegramuser',
            name='smartup_id',
        ),

        # --- QRCode changes ---
        migrations.RemoveField(
            model_name='qrcode',
            name='code_type',
        ),
        migrations.RemoveField(
            model_name='historicalqrcode',
            name='code_type',
        ),
        migrations.AddField(
            model_name='qrcode',
            name='store',
            field=models.ForeignKey(blank=True, null=True, db_index=True, on_delete=django.db.models.deletion.PROTECT, related_name='qr_codes', to='core.store', verbose_name="Do'kon"),
        ),
        migrations.AddField(
            model_name='historicalqrcode',
            name='store',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='core.store', verbose_name="Do'kon"),
        ),
        migrations.AddField(
            model_name='qrcode',
            name='batch',
            field=models.ForeignKey(blank=True, null=True, db_index=True, on_delete=django.db.models.deletion.PROTECT, related_name='qr_codes', to='core.qrcodebatch', verbose_name='Batch'),
        ),
        migrations.AddField(
            model_name='historicalqrcode',
            name='batch',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='core.qrcodebatch', verbose_name='Batch'),
        ),
        migrations.AlterField(
            model_name='qrcode',
            name='scanned_by',
            field=models.ForeignKey(blank=True, limit_choices_to={'user_type': 'santenik'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='scanned_qrcodes', to='core.telegramuser'),
        ),
        migrations.AlterField(
            model_name='qrcode',
            name='is_scanned',
            field=models.BooleanField(db_index=True, default=False),
        ),

        # --- Gift changes ---
        migrations.RemoveField(
            model_name='gift',
            name='user_type',
        ),
        migrations.RemoveField(
            model_name='historicalgift',
            name='user_type',
        ),
        migrations.AddField(
            model_name='gift',
            name='stock_quantity',
            field=models.IntegerField(blank=True, null=True, help_text="Bo'sh qoldirilsa, cheksiz", verbose_name='Zaxira miqdori'),
        ),
        migrations.AddField(
            model_name='historicalgift',
            name='stock_quantity',
            field=models.IntegerField(blank=True, null=True, help_text="Bo'sh qoldirilsa, cheksiz", verbose_name='Zaxira miqdori'),
        ),

        # --- GiftRedemption limit to santenik ---
        migrations.AlterField(
            model_name='giftredemption',
            name='user',
            field=models.ForeignKey(limit_choices_to={'user_type': 'santenik'}, on_delete=django.db.models.deletion.CASCADE, related_name='gift_redemptions', to='core.telegramuser', verbose_name='Member'),
        ),

        # --- MonthlyPromoTicket: add store ---
        migrations.AddField(
            model_name='monthlypromoticket',
            name='store',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='monthly_tickets', to='core.store', verbose_name="Do'kon"),
        ),
        migrations.AddField(
            model_name='historicalmonthlypromoticket',
            name='store',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='core.store', verbose_name="Do'kon"),
        ),
        migrations.AlterField(
            model_name='monthlypromoticket',
            name='user_type',
            field=models.CharField(choices=[('santenik', 'Santenik'), ('sotuvchi', 'Sotuvchi')], db_index=True, default='santenik', max_length=20, verbose_name='Foydalanuvchi turi'),
        ),

        # --- BroadcastMessage: add store_filter, update user_type_filter ---
        migrations.AddField(
            model_name='broadcastmessage',
            name='store_filter',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='broadcasts', to='core.store', verbose_name="Do'kon bo'yicha filtr", help_text="Tanlangan do'kon foydalanuvchilariga (sotuvchilar yoki uning santeniklariga)."),
        ),
        migrations.AddField(
            model_name='historicalbroadcastmessage',
            name='store_filter',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='core.store', verbose_name="Do'kon bo'yicha filtr"),
        ),
        migrations.AlterField(
            model_name='broadcastmessage',
            name='user_type_filter',
            field=models.CharField(blank=True, choices=[('santenik', 'Santenik'), ('sotuvchi', 'Sotuvchi')], max_length=20, null=True, verbose_name="Foydalanuvchi turi bo'yicha filtr"),
        ),

        # --- SellerPointsTransaction model ---
        migrations.CreateModel(
            name='SellerPointsTransaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('transaction_type', models.CharField(choices=[('manual_add', "Admin qo'shdi"), ('sales_bonus', 'Sotuv bonusi'), ('correction', 'Tuzatish'), ('penalty', 'Jarima')], default='manual_add', max_length=20, verbose_name='Tur')),
                ('points', models.IntegerField(help_text="Musbat — qo'shish, manfiy — ayirish", verbose_name='Ballar')),
                ('sales_amount_usd', models.DecimalField(blank=True, decimal_places=2, help_text="Tranzaksiya bog'liq sotuv summasi (ixtiyoriy)", max_digits=12, null=True, verbose_name='Sotuv summasi ($)')),
                ('period_start', models.DateField(blank=True, null=True, verbose_name='Davr (boshlanish)')),
                ('period_end', models.DateField(blank=True, null=True, verbose_name='Davr (tugash)')),
                ('note', models.TextField(blank=True, verbose_name='Izoh')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='seller_transactions_created', to=settings.AUTH_USER_MODEL, verbose_name="Kim qo'shgan")),
                ('seller', models.ForeignKey(limit_choices_to={'user_type': 'sotuvchi'}, on_delete=django.db.models.deletion.PROTECT, related_name='seller_transactions', to='core.telegramuser', verbose_name='Sotuvchi')),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='seller_transactions', to='core.store', verbose_name="Do'kon")),
            ],
            options={
                'verbose_name': 'Sotuvchi tranzaksiyasi',
                'verbose_name_plural': 'Sotuvchi tranzaksiyalari',
                'ordering': ['-created_at'],
                'indexes': [
                    models.Index(fields=['seller', '-created_at'], name='core_seller_seller_idx'),
                    models.Index(fields=['store', '-created_at'], name='core_seller_store_idx'),
                ],
                'permissions': [('add_seller_points', 'Can add points to seller')],
            },
        ),

        # Historical model for SellerPointsTransaction
        migrations.CreateModel(
            name='HistoricalSellerPointsTransaction',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('transaction_type', models.CharField(choices=[('manual_add', "Admin qo'shdi"), ('sales_bonus', 'Sotuv bonusi'), ('correction', 'Tuzatish'), ('penalty', 'Jarima')], default='manual_add', max_length=20, verbose_name='Tur')),
                ('points', models.IntegerField(help_text="Musbat — qo'shish, manfiy — ayirish", verbose_name='Ballar')),
                ('sales_amount_usd', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True, verbose_name='Sotuv summasi ($)')),
                ('period_start', models.DateField(blank=True, null=True, verbose_name='Davr (boshlanish)')),
                ('period_end', models.DateField(blank=True, null=True, verbose_name='Davr (tugash)')),
                ('note', models.TextField(blank=True, verbose_name='Izoh')),
                ('created_at', models.DateTimeField(blank=True, editable=False)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('created_by', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name="Kim qo'shgan")),
                ('seller', models.ForeignKey(blank=True, db_constraint=False, limit_choices_to={'user_type': 'sotuvchi'}, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='core.telegramuser', verbose_name='Sotuvchi')),
                ('store', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='core.store', verbose_name="Do'kon")),
            ],
            options={
                'verbose_name': 'historical Sotuvchi tranzaksiyasi',
                'verbose_name_plural': 'historical Sotuvchi tranzaksiyalari',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),

        # --- Indexes update on Gift (was user_type+is_active, now just is_active) ---
        migrations.RemoveIndex(
            model_name='gift',
            name='core_gift_user_ty_d6f10b_idx',
        ),
        migrations.AddIndex(
            model_name='gift',
            index=models.Index(fields=['is_active'], name='core_gift_is_acti_idx'),
        ),
    ]
