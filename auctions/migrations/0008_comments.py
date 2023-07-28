# Generated by Django 4.2.3 on 2023-07-28 08:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0007_listing_watchlist"),
    ]

    operations = [
        migrations.CreateModel(
            name="comments",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("comment", models.CharField(max_length=500)),
                (
                    "comment_listing",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="listingcomments",
                        to="auctions.listing",
                    ),
                ),
                (
                    "comment_user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="usercomments",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
