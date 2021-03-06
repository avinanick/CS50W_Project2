from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, AuctionListing, AuctionBid, Comment
from .utils import calculate_price
from .forms import ListingForm, BidForm, CommentForm, Category



def category_listings(request, category):
    category = Category.objects.get(type=category)
    auctions = AuctionListing.objects.filter(category=category, is_active=True)
    return render(request, "auctions/category_listings.html", {
        "category": category,
        "listings": auctions
    })

@login_required
def create_listing(request):
    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():
            new_listing = AuctionListing(title=form.cleaned_data["title"],
                                            description=form.cleaned_data["description"],
                                            starting_bid=form.cleaned_data["starting_bid"],
                                            price=form.cleaned_data["starting_bid"],
                                            image_url=form.cleaned_data["image_url"],
                                            poster=request.user,
                                            category=form.cleaned_data["category"])
            new_listing.save()
            return redirect("listing", listing_id=new_listing.id)

    return render(request, "auctions/create_listing.html", {
        "form": ListingForm()
    })

def index(request):
    return render(request, "auctions/index.html", {
        "active_listings": AuctionListing.objects.filter(is_active=True)
    })

def list_categories(request):
    return render(request, "auctions/list_categories.html", {
        "categories": Category.objects.all()
    })

def listing_view(request, listing_id):
    auction = AuctionListing.objects.get(id=listing_id)
    var_dict = {
        "form": BidForm(),
        "listing": auction,
        "comment_form": CommentForm(),
        "comments": auction.listing_comments.all()
    }
    if request.method == "POST":
        if request.user.is_authenticated:
            if "bid" in request.POST:
                form = BidForm(request.POST)
                if form.is_valid():
                    if auction.price < form.cleaned_data["bid"]:
                        auction.price = form.cleaned_data["bid"]
                        auction.save()
                        new_bid = AuctionBid(listing=auction,
                            bidder=request.user,
                            amount=form.cleaned_data["bid"])
                        new_bid.save()
                    else:
                        var_dict["form"] = form
                        var_dict["message"] = "You must enter a bid that is higher than the current highest bid!"
            if "comment" in request.POST:
                comment_form = CommentForm(request.POST)
                if comment_form.is_valid():
                    new_comment = Comment(poster=request.user,
                                            listing=auction,
                                            text=comment_form.cleaned_data["comment"])
                    new_comment.save()
            if "close" in request.POST:
                auction.is_active = False
                auction.save()
    if not auction.is_active:
        winning_bid = AuctionBid.objects.get(listing=auction, amount=auction.price)
        if winning_bid:
            var_dict["winner"] = winning_bid.bidder
    return render(request, "auctions/listing_view.html", var_dict)

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def wishlist(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            auctionID = request.POST["id"]
            auction = AuctionListing.objects.get(id=auctionID)
            auction.watchers.add(request.user)
    return render(request, "auctions/wishlist.html", {
        "watchlist": request.user.watchlist.all()
    })