# Generated by Django 3.2 on 2022-04-21 22:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0003_asset_media'),
    ]

    operations = [
        migrations.AddField(
            model_name='asset',
            name='is_audio',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AddField(
            model_name='asset',
            name='is_video',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
