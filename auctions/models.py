from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Comment(models.Model):
    poster = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=1920)

class AuctionListing(models.Model):
    name = models.CharField(max_length=128)
    image_url = models.CharField(max_length=128)
    poster = models.ForeignKey(User, on_delete=models.CASCADE)

class AuctionBid(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE)
    amount = models.FloatField()