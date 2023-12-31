# Generated by Django 4.2.3 on 2023-07-28 06:07

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0006_rename_category_category_categoryname"),
    ]

    operations = [
        migrations.AddField(
            model_name="listing",
            name="watchlist",
            field=models.ManyToManyField(
                blank=True,
                null=True,
                related_name="intrested_watchlist",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
