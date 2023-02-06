# Generated by Django 3.2.16 on 2023-01-23 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0006_auto_20230105_2356'),
    ]

    operations = [
        migrations.AlterField(
            model_name='escrow',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=255),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=255),
        ),
        migrations.AlterField(
            model_name='wallet',
            name='balance',
            field=models.DecimalField(decimal_places=2, max_digits=255),
        ),
    ]