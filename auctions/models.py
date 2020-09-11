from django.contrib.auth.models import AbstractUser
from django.db import models


class AuctionListing(models.Model):
    pass

class AuctionBid(models.Model):
    pass

class Comment(models.Model):
    pass

class User(AbstractUser):
    pass
