# Generated by Django 3.2 on 2022-04-21 21:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0002_auto_20220308_1912'),
    ]

    operations = [
        migrations.AddField(
            model_name='asset',
            name='media',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]
