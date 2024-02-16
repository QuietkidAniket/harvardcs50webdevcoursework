#important import
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
# Create your views here.
def index(request):
    #display the information about the currently signed in user
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))#redirects to login route
    return render(request, "users/user.html")#renders the user.html page


def login_view(request):
    if request.method == "POST":
        #accessing username and password from form data
        username = request.POST["username"]
        password = request.POST["password"]
        #checking if username and password are correct, returning a user object if so
        user = authenticate(request, username = username, password = password)
        #if the user object is returned, then login and reroute to index page
        if user:
            login(request, user) #logs in
            return HttpResponseRedirect(reverse("index"))#redirects to index route
        else:
        #else return a login page again with new context
            return render(request,"users/login.html", {
                "message" : "Invalid Credentials"
            })
    return render(request, "users/login.html")


def logout_view(request):
    logout(request) #logs out
    #renders login.html with a "logged out" message
    return render(request, "users/login.html", { 
        "message" : "Logged out" 
    })