# Generated by Django 5.2.1 on 2025-05-29 21:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='usercity',
            name='count',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
