from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User, Listing, Comment, Category, Bid, Picture

def index(request):
    if not request.user.is_authenticated :
        return HttpResponseRedirect("login")
    watchlistlength = len(list(request.user.spectators_list.all()))
    listings = Listing.objects.exclude(flactive = False).all()
    for listing in listings:
        defaultimage = listing.get_pictures.first()
        if request.user in listing.spectators.all() :
            listing.watching = True
        else :
            listing.watching = False
    categories = Category.objects.all()
    return render(request, "auctions/index.html", {
        "heading" : "Active Listings",
        "defaultimage" : defaultimage,
        "activelistings" : listings,
        "categories" : categories,
        "watchlistlength" : watchlistlength,
        "error_message": "No Active Listings"
    })


@login_required
def listing(request, title):
    watchlist = request.user.spectators_list.all()
    watchlistlength = len(watchlist)
    listing = Listing.objects.get(title = title)
    if request.user in listing.spectators.all() :
        listing.watching = True
    else :
        listing.watching = False
    return render(request, "auctions/listing.html", {
        "listing"  : listing,
        "watchlistlength" : watchlistlength,
        "iswatching" : listing.watching
    })

def newlisting(request):
    pass

def categories(request):
    categories = Category.objects.all()
    return render(request, "auctions/categories.html", {
        "categories" : categories
    })

def categorylistings(request, category_name):
    watchlistlength = len(list(request.user.spectators_list.all()))
    listings = Listing.objects.filter(category = Category.objects.get(category = category_name).id).all()  
    return render(request, "auctions/categorylistings.html", {
        "heading" : f"{category_name}",
        "watchlistlength": watchlistlength,
        "activelistings":listings,
        "category_name" : category_name,
        "error_message" : "No listings under this category"
    })

def watchlist(request):
    watchlist = request.user.spectators_list.all()
    watchlistlength = len(watchlist)
    return render(request, "auctions/watchlist.html", {
        "heading" : "Watchlist",
        "watchlist" : watchlist,
        "watchlistlength" : watchlistlength,
        "error_message":"No Active listing in your watchlist"
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
