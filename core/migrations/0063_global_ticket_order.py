"""
Меняет порядок нумерации билетов MonthlyPromoTicket:
было: order сбрасывался каждый месяц (ключ: month + user_type)
стало: order глобальный по user_type (не сбрасывается при смене месяца)

Шаги:
1. Удалить старый constraint (month, user_type, order)
2. Перенумеровать все билеты глобально по user_type (по возрастанию scanned_at)
3. Добавить новый constraint (user_type, order)
"""
from __future__ import annotations

from collections import defaultdict

from django.db import migrations, models


def _renumber_globally(apps, schema_editor):
    MonthlyPromoTicket = apps.get_model('core', 'MonthlyPromoTicket')

    counters: dict[str, int] = defaultdict(int)
    to_update = []

    qs = MonthlyPromoTicket.objects.order_by('scanned_at', 'id')
    for ticket in qs.iterator(chunk_size=2000):
        ut = ticket.user_type or 'electrician'
        counters[ut] += 1
        ticket.order = counters[ut]
        to_update.append(ticket)
        if len(to_update) >= 2000:
            MonthlyPromoTicket.objects.bulk_update(to_update, ['order'], batch_size=2000)
            to_update = []

    if to_update:
        MonthlyPromoTicket.objects.bulk_update(to_update, ['order'], batch_size=2000)


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0062_alter_promotion_date'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='monthlypromoticket',
            name='uniq_monthly_ticket_order_per_type',
        ),
        migrations.AlterField(
            model_name='monthlypromoticket',
            name='order',
            field=models.PositiveIntegerField(
                db_index=True,
                verbose_name='Bilet №',
                help_text='Глобальный порядковый номер билета по user_type (не сбрасывается каждый месяц).',
            ),
        ),
        migrations.AlterField(
            model_name='historicalmonthlypromoticket',
            name='order',
            field=models.PositiveIntegerField(
                db_index=True,
                verbose_name='Bilet №',
                help_text='Глобальный порядковый номер билета по user_type (не сбрасывается каждый месяц).',
            ),
        ),
        migrations.RunPython(_renumber_globally, reverse_code=migrations.RunPython.noop),
        migrations.AddConstraint(
            model_name='monthlypromoticket',
            constraint=models.UniqueConstraint(
                fields=('user_type', 'order'),
                name='uniq_ticket_order_global_per_type',
            ),
        ),
    ]
