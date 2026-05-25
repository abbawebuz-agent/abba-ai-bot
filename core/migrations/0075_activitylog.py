"""ActivityLog — centralized audit log."""
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0074_simplify_status_active_inactive'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActivityLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Vaqt')),
                ('action_type', models.CharField(
                    choices=[
                        ('login', '🔓 Tizimga kirish'),
                        ('logout', '🔒 Chiqish'),
                        ('login_failed', '❌ Kirish xato'),
                        ('create', '➕ Yaratildi'),
                        ('update', '✏️ Yangilandi'),
                        ('delete', '🗑️ O‘chirildi'),
                        ('backup', '💾 Backup'),
                        ('export', '📤 Export'),
                        ('webhook', '🤖 Webhook'),
                        ('admin_action', '⚙️ Admin amal'),
                        ('error', '⚠️ Xato'),
                        ('custom', '📝 Boshqa'),
                    ],
                    db_index=True, default='custom', max_length=30, verbose_name='Amal turi',
                )),
                ('target_model', models.CharField(
                    blank=True, db_index=True, max_length=100,
                    help_text='Masalan: QRCodeBatch, TelegramUser',
                    verbose_name='Obyekt turi',
                )),
                ('target_id', models.PositiveIntegerField(blank=True, null=True, verbose_name='Obyekt ID')),
                ('target_repr', models.CharField(blank=True, max_length=255, verbose_name='Obyekt')),
                ('description', models.TextField(blank=True, verbose_name='Tavsif')),
                ('metadata', models.JSONField(blank=True, default=dict, verbose_name='Qo‘shimcha')),
                ('ip_address', models.GenericIPAddressField(blank=True, null=True, verbose_name='IP')),
                ('user_agent', models.CharField(blank=True, max_length=500, verbose_name='Brauzer')),
                ('user', models.ForeignKey(
                    blank=True, null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    related_name='activity_logs',
                    to=settings.AUTH_USER_MODEL,
                    verbose_name='Kim',
                )),
                ('tg_user', models.ForeignKey(
                    blank=True, null=True,
                    help_text='Bot orqali amal qilgan foydalanuvchi',
                    on_delete=django.db.models.deletion.SET_NULL,
                    related_name='activity_logs',
                    to='core.telegramuser',
                    verbose_name='Telegram foydalanuvchi',
                )),
            ],
            options={
                'verbose_name': 'Log yozuvi',
                'verbose_name_plural': 'Faollik tarixi (Audit log)',
                'ordering': ['-timestamp'],
                'indexes': [
                    models.Index(fields=['-timestamp'], name='core_activi_timesta_idx'),
                    models.Index(fields=['user', '-timestamp'], name='core_activi_user_ts_idx'),
                    models.Index(fields=['action_type', '-timestamp'], name='core_activi_action_idx'),
                    models.Index(fields=['target_model', 'target_id'], name='core_activi_target_idx'),
                ],
            },
        ),
    ]
