"""Fix: core_historicalqrcode table'ga `sequence_number` column qo'shish.

Migration 0076 QRCode.sequence_number qo'shgan, lekin simple_history'ning
historical jadvali (`core_historicalqrcode`)ga column qo'shilmagan.
Natijada `QRCode.objects.create(..., sequence_number=...)` ProgrammingError
bermoqda chunki post_save signal historical insertni amalga oshira olmaydi.
"""
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0077_claudeinbox'),
    ]

    operations = [
        migrations.RunSQL(
            sql=(
                "ALTER TABLE core_historicalqrcode "
                "ADD COLUMN IF NOT EXISTS sequence_number INTEGER NULL;"
            ),
            reverse_sql=(
                "ALTER TABLE core_historicalqrcode "
                "DROP COLUMN IF EXISTS sequence_number;"
            ),
        ),
        # Index ham qo'shamiz (historical jadvalda search uchun)
        migrations.RunSQL(
            sql=(
                "CREATE INDEX IF NOT EXISTS "
                "core_historicalqrcode_sequence_number_idx "
                "ON core_historicalqrcode (sequence_number);"
            ),
            reverse_sql=(
                "DROP INDEX IF EXISTS "
                "core_historicalqrcode_sequence_number_idx;"
            ),
        ),
    ]
