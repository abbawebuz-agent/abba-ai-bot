"""Partiya status: 4/3 ta holat → 2 ta (active/inactive).

Old → New mapping:
- status: completed → active; pending/processing/failed → inactive
- delivery_status: delivered → active; shipped/not_shipped → inactive
"""
from django.db import migrations, models


def forward(apps, schema_editor):
    QRCodeBatch = apps.get_model('core', 'QRCodeBatch')

    # status mapping
    QRCodeBatch.objects.filter(status='completed').update(status='active')
    QRCodeBatch.objects.exclude(status='active').update(status='inactive')

    # delivery_status mapping
    QRCodeBatch.objects.filter(delivery_status='delivered').update(delivery_status='active')
    QRCodeBatch.objects.exclude(delivery_status='active').update(delivery_status='inactive')


def backward(apps, schema_editor):
    # Best-effort reverse — barchasini pending/not_shipped ga qaytarish
    QRCodeBatch = apps.get_model('core', 'QRCodeBatch')
    QRCodeBatch.objects.filter(status='active').update(status='completed')
    QRCodeBatch.objects.filter(status='inactive').update(status='pending')
    QRCodeBatch.objects.filter(delivery_status='active').update(delivery_status='delivered')
    QRCodeBatch.objects.filter(delivery_status='inactive').update(delivery_status='not_shipped')


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0073_store_optional_seller_direct'),
    ]

    operations = [
        # 1) Avval qiymatlarni map qilamiz (eski choices bilan)
        migrations.RunPython(forward, backward),
        # 2) Endi schema choices yangilanadi
        migrations.AlterField(
            model_name='qrcodebatch',
            name='status',
            field=models.CharField(
                choices=[('active', 'Faollashtirilgan'), ('inactive', 'Faollashtirilmagan')],
                default='inactive',
                max_length=20,
                verbose_name='Holat',
            ),
        ),
        migrations.AlterField(
            model_name='historicalqrcodebatch',
            name='status',
            field=models.CharField(
                choices=[('active', 'Faollashtirilgan'), ('inactive', 'Faollashtirilmagan')],
                default='inactive',
                max_length=20,
                verbose_name='Holat',
            ),
        ),
        migrations.AlterField(
            model_name='qrcodebatch',
            name='delivery_status',
            field=models.CharField(
                choices=[('active', 'Faollashtirilgan'), ('inactive', 'Faollashtirilmagan')],
                default='inactive',
                max_length=20,
                verbose_name='Yetkazib berish holati',
            ),
        ),
        migrations.AlterField(
            model_name='historicalqrcodebatch',
            name='delivery_status',
            field=models.CharField(
                choices=[('active', 'Faollashtirilgan'), ('inactive', 'Faollashtirilmagan')],
                default='inactive',
                max_length=20,
                verbose_name='Yetkazib berish holati',
            ),
        ),
    ]
