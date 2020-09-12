from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import User, AuctionListing, AuctionBid, Comment
from .utils import calculate_price
from .forms import ListingForm, BidForm



def create_listing(request):
    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():
            new_listing = AuctionListing(title=form.cleaned_data["title"],
                                            description=form.cleaned_data["description"],
                                            starting_bid=form.cleaned_data["starting_bid"],
                                            price=form.cleaned_data["starting_bid"],
                                            image_url=form.cleaned_data["image_url"],
                                            poster=request.user)
            new_listing.save()
            return redirect("listing", listing_id=new_listing.id)

    return render(request, "auctions/create_listing.html", {
        "form": ListingForm()
    })

def index(request):
    return render(request, "auctions/index.html", {
        "active_listings": AuctionListing.objects.all()
    })

def listing_view(request, listing_id):
    if request.method == "POST":
        if request.user.is_authenticated
    auction = AuctionListing.objects.get(id=listing_id)
    return render(request, "auctions/listing_view.html", {
        "listing": auction
    })

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

def wishlist(request):
    return render(request, "auctions/wishlist.html")