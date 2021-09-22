# Generated by Django 3.1.4 on 2021-09-17 01:45

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20210915_0846'),
    ]

    operations = [
        migrations.AddField(
            model_name='userbase',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]