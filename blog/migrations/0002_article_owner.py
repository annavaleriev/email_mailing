# Generated by Django 5.0.7 on 2024-08-26 17:28

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="article",
            name="owner",
            field=models.ForeignKey(
                default=2,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="articles",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Автор",
            ),
            preserve_default=False,
        ),
    ]
