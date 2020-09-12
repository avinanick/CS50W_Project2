from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class AuctionListing(models.Model):
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=1920)
    starting_bid = models.FloatField()
    price = models.FloatField()
    image_url = models.CharField(max_length=128)
    poster = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")

class Comment(models.Model):
    poster = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comments")
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="listing_comments")
    text = models.CharField(max_length=1920)

class AuctionBid(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="listing_bids")
    amount = models.FloatField()