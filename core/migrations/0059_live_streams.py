# Generated for LiveStream feature

import django.db.models.deletion
import simple_history.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0058_backfill_monthly_promo_tickets'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='LiveStream',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_uz_latin', models.CharField(max_length=255, verbose_name="Sarlavha (O'zbek lotin)")),
                ('title_ru', models.CharField(blank=True, max_length=255, verbose_name='Sarlavha (Ruscha)')),
                ('description_uz_latin', models.TextField(blank=True, verbose_name="Tavsif (O'zbek lotin)")),
                ('description_ru', models.TextField(blank=True, verbose_name='Tavsif (Ruscha)')),
                ('scheduled_at', models.DateTimeField(db_index=True, verbose_name='Efir vaqti')),
                ('stream_url', models.URLField(help_text='Telegram/YouTube va boshqa havola', verbose_name='Efir havolasi')),
                ('cover', models.ImageField(blank=True, null=True, upload_to='live_streams/', verbose_name='Muqova')),
                ('is_active', models.BooleanField(db_index=True, default=True, verbose_name='Faol')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Jonli efir',
                'verbose_name_plural': 'Jonli efirlar',
                'ordering': ['-scheduled_at'],
            },
        ),
        migrations.AddIndex(
            model_name='livestream',
            index=models.Index(fields=['is_active', 'scheduled_at'], name='core_livest_is_acti_idx'),
        ),
        migrations.CreateModel(
            name='HistoricalLiveStream',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('title_uz_latin', models.CharField(max_length=255, verbose_name="Sarlavha (O'zbek lotin)")),
                ('title_ru', models.CharField(blank=True, max_length=255, verbose_name='Sarlavha (Ruscha)')),
                ('description_uz_latin', models.TextField(blank=True, verbose_name="Tavsif (O'zbek lotin)")),
                ('description_ru', models.TextField(blank=True, verbose_name='Tavsif (Ruscha)')),
                ('scheduled_at', models.DateTimeField(db_index=True, verbose_name='Efir vaqti')),
                ('stream_url', models.URLField(help_text='Telegram/YouTube va boshqa havola', verbose_name='Efir havolasi')),
                ('cover', models.TextField(blank=True, max_length=100, null=True, verbose_name='Muqova')),
                ('is_active', models.BooleanField(db_index=True, default=True, verbose_name='Faol')),
                ('created_at', models.DateTimeField(blank=True, editable=False)),
                ('updated_at', models.DateTimeField(blank=True, editable=False)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.TextField(null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical Jonli efir',
                'verbose_name_plural': 'historical Jonli efirlar',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='LiveStreamWinner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prize_text_uz_latin', models.CharField(blank=True, max_length=255, verbose_name="Sovg'a (O'zbek lotin)")),
                ('prize_text_ru', models.CharField(blank=True, max_length=255, verbose_name="Sovg'a (Ruscha)")),
                ('position', models.PositiveIntegerField(default=0, verbose_name='Tartib raqami')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('live_stream', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='winners', to='core.livestream', verbose_name='Jonli efir')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='live_stream_wins', to='core.telegramuser', verbose_name="G'olib")),
            ],
            options={
                'verbose_name': "Jonli efir g'olibi",
                'verbose_name_plural': "Jonli efir g'oliblari",
                'ordering': ['live_stream', 'position', 'id'],
            },
        ),
        migrations.AddIndex(
            model_name='livestreamwinner',
            index=models.Index(fields=['live_stream', 'position'], name='core_livest_live_st_pos_idx'),
        ),
        migrations.CreateModel(
            name='HistoricalLiveStreamWinner',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('prize_text_uz_latin', models.CharField(blank=True, max_length=255, verbose_name="Sovg'a (O'zbek lotin)")),
                ('prize_text_ru', models.CharField(blank=True, max_length=255, verbose_name="Sovg'a (Ruscha)")),
                ('position', models.PositiveIntegerField(default=0, verbose_name='Tartib raqami')),
                ('created_at', models.DateTimeField(blank=True, editable=False)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.TextField(null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('live_stream', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='core.livestream', verbose_name='Jonli efir')),
                ('user', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='core.telegramuser', verbose_name="G'olib")),
            ],
            options={
                'verbose_name': "historical Jonli efir g'olibi",
                'verbose_name_plural': "historical Jonli efir g'oliblari",
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
