from .models import User, AuctionListing, AuctionBid, Comment

def calculate_price(auction):
    highest_bid = auction.listing_bids.order_by("-amount").first()
    price = auction.starting_bid
    if highest_bid:
        price = highest_bid
    return price