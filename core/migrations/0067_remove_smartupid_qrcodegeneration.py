"""Remove SmartUPId and QRCodeGeneration models (replaced by QRCodeBatch in JIP)."""
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0066_jip_loyalty_models'),
    ]

    operations = [
        # Remove HistoricalQRCodeGeneration first (history table)
        migrations.DeleteModel(
            name='HistoricalQRCodeGeneration',
        ),
        # Remove M2M between QRCodeGeneration and QRCode
        migrations.RemoveField(
            model_name='QRCodeGeneration',
            name='qr_codes',
        ),
        migrations.RemoveField(
            model_name='QRCodeGeneration',
            name='created_by',
        ),
        migrations.DeleteModel(
            name='QRCodeGeneration',
        ),
        migrations.DeleteModel(
            name='SmartUPId',
        ),
    ]
