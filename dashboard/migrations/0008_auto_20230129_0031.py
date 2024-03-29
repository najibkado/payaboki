# Generated by Django 3.2.16 on 2023-01-28 23:31

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0007_auto_20230123_1417'),
    ]

    operations = [
        migrations.AddField(
            model_name='escrow',
            name='ref',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
        migrations.AddField(
            model_name='transaction',
            name='ref',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
