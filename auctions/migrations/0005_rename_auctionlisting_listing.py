# Generated by Django 4.2.3 on 2023-07-27 01:46

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0004_rename_current_bid_auctionlisting_price_and_more"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="AuctionListing",
            new_name="listing",
        ),
    ]
