# Generated by Django 2.2.12 on 2020-05-12 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20200512_0835'),
    ]

    operations = [
        migrations.AddField(
            model_name='ctask',
            name='status',
            field=models.CharField(blank=True, max_length=100, verbose_name='status'),
        ),
    ]