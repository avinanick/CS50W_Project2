# Generated by Django 3.1 on 2020-09-12 23:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_auto_20200912_2337'),
    ]

    operations = [
        migrations.AddField(
            model_name='auctionlisting',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
