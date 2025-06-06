# Generated by Django 5.0.9 on 2025-01-19 09:05

import django.db.models.deletion
import django.utils.timezone
import jsonfield.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.CharField(choices=[('success', 'success'), ('info', 'info'), ('warning', 'warning'), ('error', 'error')], default='info', max_length=20, verbose_name='level')),
                ('unread', models.BooleanField(db_index=True, default=True, verbose_name='unread')),
                ('actor_object_id', models.CharField(max_length=255, verbose_name='actor object id')),
                ('verb', models.CharField(max_length=255, verbose_name='verb')),
                ('description', models.TextField(blank=True, null=True, verbose_name='description')),
                ('target_object_id', models.CharField(blank=True, max_length=255, null=True, verbose_name='target object id')),
                ('action_object_object_id', models.CharField(blank=True, max_length=255, null=True, verbose_name='action object object id')),
                ('timestamp', models.DateTimeField(db_index=True, default=django.utils.timezone.now, verbose_name='timestamp')),
                ('public', models.BooleanField(db_index=True, default=True, verbose_name='public')),
                ('deleted', models.BooleanField(db_index=True, default=False, verbose_name='deleted')),
                ('emailed', models.BooleanField(db_index=True, default=False, verbose_name='emailed')),
                ('data', jsonfield.fields.JSONField(blank=True, null=True, verbose_name='data')),
                ('push_notification', models.BooleanField(default=False)),
                ('action_object_content_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notify_action_object', to='contenttypes.contenttype', verbose_name='action object content type')),
                ('actor_content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notify_actor', to='contenttypes.contenttype', verbose_name='actor content type')),
            ],
            options={
                'verbose_name': 'Notification',
                'verbose_name_plural': 'Notifications',
                'ordering': ('-timestamp',),
                'abstract': False,
            },
        ),
    ]
