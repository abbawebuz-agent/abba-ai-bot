from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0049_qrcode_is_deleted'),
    ]

    operations = [
        migrations.CreateModel(
            name='MonthlyPromoParticipant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month', models.DateField(db_index=True, verbose_name='Oy (1-kun)')),
                ('order', models.PositiveIntegerField(db_index=True, verbose_name='Tartib raqami (oy bo‘yicha)')),
                ('first_promo_at', models.DateTimeField(verbose_name='Birinchi promokod vaqti')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='monthly_promo_participations', to='core.telegramuser', verbose_name='Member')),
            ],
            options={
                'verbose_name': 'Monthly promo participant',
                'verbose_name_plural': 'Monthly promo participants',
                'ordering': ['-month', 'order'],
            },
        ),
        migrations.AddConstraint(
            model_name='monthlypromoparticipant',
            constraint=models.UniqueConstraint(fields=('month', 'user'), name='uniq_monthly_promo_user'),
        ),
        migrations.AddConstraint(
            model_name='monthlypromoparticipant',
            constraint=models.UniqueConstraint(fields=('month', 'order'), name='uniq_monthly_promo_order'),
        ),
    ]

