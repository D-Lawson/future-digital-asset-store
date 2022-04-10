# Generated by Django 3.2 on 2022-04-10 16:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('checkout', '0003_alter_order_country'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='user_account',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='accounts.useraccount'),
        ),
    ]
