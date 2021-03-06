# Generated by Django 2.2.12 on 2020-07-05 01:55

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20200628_0006'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_json', django.contrib.postgres.fields.jsonb.JSONField(verbose_name='ClickUp JSON Response')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attachments', to='core.Task')),
            ],
        ),
    ]
