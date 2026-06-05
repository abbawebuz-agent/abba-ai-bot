from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0083_projectphoto'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectphoto',
            name='caption',
            field=models.CharField(blank=True, default='', max_length=80, verbose_name='Izoh'),
        ),
        migrations.AddField(
            model_name='projectphoto',
            name='is_deleted',
            field=models.BooleanField(db_index=True, default=False, verbose_name="Usta o'chirgan"),
        ),
        migrations.AddField(
            model_name='projectphoto',
            name='deleted_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name="O'chirilgan vaqt"),
        ),
    ]
