from django.contrib import admin
from .models import AuctionListing, AuctionBid, Comment, Category

# Register your models here.
admin.site.register(AuctionListing)
admin.site.register(AuctionBid)
admin.site.register(Comment)
admin.site.register(Category)