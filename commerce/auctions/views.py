from django.forms import ModelForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError, models
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User, Listing, Comment, Category, Bid
from django.utils import timezone
def index(request):
    watchlistlength = None
    listings = Listing.objects.exclude(flactive = False).all()
    if request.user.is_authenticated :
        watchlistlength = len(list(request.user.spectators_list.all()))
        for listing in listings:
            if request.user in listing.spectators.all() :
                listing.watching = True
            else :
                listing.watching = False
    
    categories = Category.objects.all()
    return render(request, "auctions/index.html", {
        "heading" : "Active Listings",
        "activelistings" : listings,
        "categories" : categories,
        "watchlistlength" : watchlistlength,
        "error_message": "No Active Listings"
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
def categories(request):
    categories = Category.objects.all()
    return render(request, "auctions/categories.html", {
        "categories" : categories
    })


def listing(request, id):
    watchlistlength = None
    listing = Listing.objects.get(pk = id)
    listing.watching = False
    message = ""
    if not listing.flactive :
        message =  f"{listing.buyer} has won the auction with the final Bid of ${listing.currentBid}"
    if request.user.is_authenticated:
        watchlist = request.user.spectators_list.all()
        watchlistlength = len(watchlist)
        if request.user in listing.spectators.all() :
            listing.watching = True
        else :
            listing.watching = False
        if request.user == listing.buyer:
            message = f"You have won the auction with the final Bid of ${listing.currentBid}"
    comments = Comment.objects.filter(listing = listing).all()

    return render(request, "auctions/listing.html", {
        "listing"  : listing,
        "watchlistlength" : watchlistlength,
        "iswatching" : listing.watching,
        "id" : listing.pk,
        "comments" : comments,
        "message" : message
    })

@login_required
def newlisting(request):
    form = request.POST
    if request.method == 'POST':    
        creator = request.user
        newlisting = Listing(title = request.POST['title'], category = Category.objects.get(category = request.POST['category']),description = request.POST['description'], creator = creator, startingBid = request.POST['startingBid'], picture= request.POST["picture"]) 
        newlisting.save()
        return HttpResponseRedirect(reverse("index"))
    else:  
        return render(request, 'auctions/newlisting.html',{ "categories": Category.objects.all()})


def closeauction(request, id):
    listing = Listing.objects.get(pk = id)
    bids = Bid.objects.filter(auction = listing).all()
    winner_bid = None
    for bid in bids:
        print(bid)
        if bid.offer == listing.currentBid :
            listing.buyer = bid.user
    listing.flactive = False
    listing.save()
    return HttpResponseRedirect(reverse("listing", args = [id])) 

def bid(request, id):
    if request.method == "POST":
        listing = Listing.objects.get(pk = id)
        bidobj = Bid(auction = listing, user = request.user, offer = float(request.POST["bidamount"]))
        bidobj.save()
        bidamount = float(request.POST["bidamount"])
        if bidamount > listing.startingBid :
            if listing.currentBid == None or listing.currentBid < bidamount: 
                listing.currentBid = bidamount
                bidobj.iscurrent =True
                listing.save()
    return HttpResponseRedirect(reverse("listing", args = [id]))   

def comment(request, id):
    if request.method == "POST":
        commenttext = ""+request.POST["comment"]
        commentobj = Comment(comment= str(commenttext), listing = Listing.objects.get(pk = id), user = request.user)
        commentobj.save()
    return HttpResponseRedirect(reverse("listing", args = [id]))   

def addtowatchlist(request, id):
    request.user.spectators_list.add(Listing.objects.get(pk = id))
    return HttpResponseRedirect(reverse("listing", args = [id]))

def removefromwatchlist(request, id):
    listing = Listing.objects.get(pk =id)
    listing.spectators.remove(request.user.id)
    return HttpResponseRedirect(reverse("listing", args = [id]))

def watchlist(request):
    watchlist = request.user.spectators_list.all()
    watchlistlength = len(watchlist)
    return render(request, "auctions/watchlist.html", {
        "heading" : "Watchlist",
        "activelistings" : watchlist,
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
