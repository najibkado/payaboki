# Generated by Django 3.2.16 on 2023-01-28 23:38

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0011_auto_20230129_0035'),
    ]

    operations = [
        migrations.AlterField(
            model_name='escrow',
            name='ref',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='ref',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
