# Generated by Django 3.2.16 on 2023-01-28 23:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0008_auto_20230129_0031'),
    ]

    operations = [
        migrations.AlterField(
            model_name='escrow',
            name='ref',
            field=models.CharField(default='abc2ea61040b46f98afebfc866e3754b', max_length=255),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='ref',
            field=models.CharField(default='09aa731deb2344f6a918fc630aa522a4', max_length=255),
        ),
    ]
