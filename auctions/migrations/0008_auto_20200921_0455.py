# Generated by Django 3.1 on 2020-09-21 04:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_auctionlisting_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlisting',
            name='image_url',
            field=models.CharField(max_length=128, null=True),
        ),
    ]