from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0076_seller_sellerbatch'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClaudeInbox',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chat_id', models.BigIntegerField(db_index=True, verbose_name='Guruh chat ID')),
                ('chat_title', models.CharField(blank=True, max_length=255, verbose_name='Guruh nomi')),
                ('message_id', models.BigIntegerField(verbose_name='Telegram xabar ID')),
                ('sender_id', models.BigIntegerField(verbose_name='Foydalanuvchi TG ID')),
                ('sender_username', models.CharField(blank=True, max_length=255)),
                ('sender_name', models.CharField(blank=True, max_length=255)),
                ('text', models.TextField(verbose_name='Savol matni')),
                ('is_read', models.BooleanField(db_index=True, default=False, verbose_name="O'qildi")),
                ('is_answered', models.BooleanField(db_index=True, default=False, verbose_name='Javob berildi')),
                ('answer_text', models.TextField(blank=True, verbose_name='Javob matni')),
                ('answered_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
            ],
            options={
                'verbose_name': 'Claude inbox xabar',
                'verbose_name_plural': 'Claude inbox (bot mention)',
                'ordering': ['-created_at'],
                'indexes': [models.Index(fields=['is_read', '-created_at'], name='core_claude_is_read_d8e3aa_idx')],
            },
        ),
    ]
