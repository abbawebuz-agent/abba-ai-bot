from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0084_projectphoto_caption_softdelete'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicaltelegramuser',
            name='welcome_bonus_awarded',
            field=models.BooleanField(default=False, verbose_name='Xush kelibsiz boni berilgan (+30 ball)'),
        ),
        migrations.AddField(
            model_name='telegramuser',
            name='welcome_bonus_awarded',
            field=models.BooleanField(db_index=True, default=False, verbose_name='Xush kelibsiz boni berilgan (+30 ball)'),
        ),
    ]
