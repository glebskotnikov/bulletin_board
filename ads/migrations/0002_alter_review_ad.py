# Generated by Django 5.1.1 on 2024-10-06 00:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ads", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="review",
            name="ad",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="reviews",
                to="ads.ad",
                verbose_name="advertisement",
            ),
        ),
    ]
