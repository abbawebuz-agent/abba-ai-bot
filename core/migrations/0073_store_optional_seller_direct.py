"""Make store optional on QRCodeBatch and SellerPointsTransaction.

Sotuvchi-direct model: ball endi to'g'ridan-to'g'ri sotuvchiga biriktiriladi,
store nullable bo'ladi (eski data uchun saqlanadi).
"""
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0072_historicalqrcodebatch_seller'),
    ]

    operations = [
        # QRCodeBatch.store → SET_NULL, nullable
        migrations.AlterField(
            model_name='qrcodebatch',
            name='store',
            field=models.ForeignKey(
                blank=True, null=True,
                help_text="Eski tizim uchun. Yangi batch yaratishda kerak emas.",
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='batches',
                to='core.store',
                verbose_name="Do'kon (deprecated)",
            ),
        ),
        migrations.AlterField(
            model_name='historicalqrcodebatch',
            name='store',
            field=models.ForeignKey(
                blank=True, null=True, db_constraint=False,
                help_text="Eski tizim uchun. Yangi batch yaratishda kerak emas.",
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name='+',
                to='core.store',
                verbose_name="Do'kon (deprecated)",
            ),
        ),
        # SellerPointsTransaction.store → SET_NULL, nullable
        migrations.AlterField(
            model_name='sellerpointstransaction',
            name='store',
            field=models.ForeignKey(
                blank=True, null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='seller_transactions',
                to='core.store',
                verbose_name="Do'kon (deprecated)",
            ),
        ),
        migrations.AlterField(
            model_name='historicalsellerpointstransaction',
            name='store',
            field=models.ForeignKey(
                blank=True, null=True, db_constraint=False,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name='+',
                to='core.store',
                verbose_name="Do'kon (deprecated)",
            ),
        ),
        # Constraint o'zgartirish: name+store → name+seller
        migrations.RemoveConstraint(
            model_name='qrcodebatch',
            name='uniq_batch_name_per_store',
        ),
        migrations.AddConstraint(
            model_name='qrcodebatch',
            constraint=models.UniqueConstraint(
                fields=['name', 'seller'],
                name='uniq_batch_name_per_seller',
            ),
        ),
        # Index store+delivery → seller+delivery
        migrations.RemoveIndex(
            model_name='qrcodebatch',
            name='core_qrcode_store_d_idx',
        ),
        migrations.AddIndex(
            model_name='qrcodebatch',
            index=models.Index(
                fields=['seller', 'delivery_status'],
                name='qrcb_seller_deliv_idx',
            ),
        ),
    ]
