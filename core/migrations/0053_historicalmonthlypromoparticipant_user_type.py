from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0052_monthlypromoparticipant_user_type_order_per_type"),
    ]

    operations = [
        migrations.AddField(
            model_name="historicalmonthlypromoparticipant",
            name="user_type",
            field=models.CharField(
                max_length=20,
                choices=[("electrician", "Elektrik"), ("seller", "Sotuvchi")],
                null=True,
                db_index=True,
                verbose_name="Foydalanuvchi turi",
            ),
        ),
    ]

