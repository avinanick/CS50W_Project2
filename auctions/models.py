from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    type=models.CharField(max_length=64)

    def __str__(self):
        return self.type

class AuctionListing(models.Model):
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=1920)
    starting_bid = models.FloatField()
    price = models.FloatField()
    image_url = models.CharField(max_length=128)
    poster = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    watchers = models.ManyToManyField(User, related_name="watchlist")
    is_active = models.BooleanField(default=True)
    category = models.ForeignKey(Category, related_name="listings", default=Category.objects.get(type="Home"))

class Comment(models.Model):
    poster = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comments")
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="listing_comments")
    text = models.CharField(max_length=1920)

class AuctionBid(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="listing_bids")
    amount = models.FloatField()