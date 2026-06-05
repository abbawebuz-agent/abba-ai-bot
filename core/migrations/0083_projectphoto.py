import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0082_cleanup_extra_scratch_cards'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectPhoto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='projects/', verbose_name='Loyiha rasmi')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Yuklangan vaqt')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_photos', to='core.telegramuser', verbose_name='Santexnik')),
            ],
            options={
                'verbose_name': 'Loyiha rasmi',
                'verbose_name_plural': 'Loyiha rasmlari',
                'ordering': ['-created_at'],
            },
        ),
        migrations.AddIndex(
            model_name='projectphoto',
            index=models.Index(fields=['user', '-created_at'], name='core_projph_user_cr_idx'),
        ),
    ]
