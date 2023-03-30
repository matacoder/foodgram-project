# Generated by Django 3.1.7 on 2021-03-16 19:11

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0002_auto_20210312_2049"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="following",
            field=models.ManyToManyField(
                blank=True,
                related_name="his_following",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Who I follow",
            ),
        ),
    ]
