from django.db import migrations, models


def _backfill_monthly_promo_participant_user_type(apps, schema_editor):
    MonthlyPromoParticipant = apps.get_model("core", "MonthlyPromoParticipant")
    TelegramUser = apps.get_model("core", "TelegramUser")

    # Берём мапу user_id -> user_type одним запросом.
    user_type_by_id = dict(
        TelegramUser.objects.exclude(user_type__isnull=True).values_list("id", "user_type")
    )

    to_update = []
    qs = MonthlyPromoParticipant.objects.filter(user_type__isnull=True).only("id", "user_id", "user_type")
    for row in qs.iterator(chunk_size=2000):
        ut = user_type_by_id.get(row.user_id) or "electrician"
        row.user_type = ut
        to_update.append(row)
        if len(to_update) >= 2000:
            MonthlyPromoParticipant.objects.bulk_update(to_update, ["user_type"], batch_size=2000)
            to_update = []

    if to_update:
        MonthlyPromoParticipant.objects.bulk_update(to_update, ["user_type"], batch_size=2000)


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0051_alter_broadcastmessage_status_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="monthlypromoparticipant",
            name="user_type",
            field=models.CharField(
                max_length=20,
                choices=[("electrician", "Elektrik"), ("seller", "Sotuvchi")],
                null=True,
                db_index=True,
                verbose_name="Foydalanuvchi turi",
            ),
        ),
        migrations.RunPython(
            _backfill_monthly_promo_participant_user_type,
            reverse_code=migrations.RunPython.noop,
        ),
        migrations.AlterField(
            model_name="monthlypromoparticipant",
            name="user_type",
            field=models.CharField(
                max_length=20,
                choices=[("electrician", "Elektrik"), ("seller", "Sotuvchi")],
                db_index=True,
                verbose_name="Foydalanuvchi turi",
            ),
        ),
        migrations.RemoveConstraint(
            model_name="monthlypromoparticipant",
            name="uniq_monthly_promo_order",
        ),
        migrations.AddConstraint(
            model_name="monthlypromoparticipant",
            constraint=models.UniqueConstraint(
                fields=("month", "user_type", "order"),
                name="uniq_monthly_promo_order_per_type",
            ),
        ),
    ]

