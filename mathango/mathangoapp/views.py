from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import User, UserStats, Game, Follow, Message
import random

# Create your views here.

def index(request):
    user = request.user 
    
    if user.is_authenticated :
        userstatobj = None
        games = None
        try:
            userstatobj = UserStats.objects.get(user = user)
            games = user.games.all()
            if games != None:
                avg_response_time = 0.0
                total_wrong = 0
                total_right = 0
                rw = 0.0
                counter = 0.0
                for game in games:
                    counter += game.avg_response_time
                    if game.right : 
                        total_right += 1
                    else:
                        total_wrong += 1
                avg_response_time = float(counter/ len(games))
                rw = float(total_right/total_wrong)
                userstatobj.user=user
                userstatobj.avg_response_time = avg_response_time, 
                userstatobj.rw = rw 
                userstatobj.total_right = total_right  
                userstatobj.total_wrong = total_wrong 
                userstatobj.save()
            
        except:
            if games == None:   
                userstatobj = UserStats(user=user, avg_response_time = 0.0, rw = 0.0, total_right = 0, total_wrong =0) 
                userstatobj.save()
            else:
                avg_response_time = 0.0
                total_wrong = 0
                total_right = 0
                rw = 0.0
                counter = 0.0
                for game in games:
                    counter += game.avg_response_time
                    if game.right : 
                        total_right += 1
                    else:
                        total_wrong += 1
                avg_response_time = float(counter/ len(games))
                rw = float(total_right/total_wrong)
                userstatobj = UserStats(user=user, avg_response_time = avg_response_time, rw = rw, total_right = total_right, total_wrong = total_wrong) 
                userstatobj.save()
        finally:
            return render(request, "mathangoapp/index.html")
    else:
        return HttpResponseRedirect("login")


def creategame(request):
    if request.method == 'GET':
        
        time = int(request.GET.get('time'))
        gameid = 0
        #creating a new game
        #obj = Game(player = request.user, questions = question[dif])
        #obj.save()
        #gameid = obj.id
        return render(request, "mathangoapp/game.html", {
            "customtime" : time,
            "gameid" : gameid
        })

    else:
        return HttpResponse("Invalid Request", 404)
        
def search(request):
    username= request.POST["search-query"]
    profile(request, username)

def leaderboard(request):
    pass

def game(request):
    if request.method == "GET":        
        c = int((10**3) - 1)
        list1 = list(range(1,c+1))
        list2 = ['a','s', 'm', 'd']
        a = random.choice(list1)
        b = None
        sign = random.choice(list2)
        ans = None
        if sign == 'a' or sign == 's':
            b = random.choice(list1)
            if sign == 'a':
                ans = a + b
                sign1 = '+'
            elif sign == 's':
                ans = a - b
                sign1 = '-'
        elif sign == 'm' or sign == 'd':
            b = random.choice(list(range(1, 10)))
            if sign == 'm':
                ans = int(a * b)
                sign1 = 'x'
            elif sign == 'd':
                if a%b != 0:
                    a = a- (a%b) 
                ans = int(a / b)
                sign1 = '%'
                    
                    
        
                

        return JsonResponse({
            "a" : a,
            "b" : b,
            "sign" : sign1,
            "ans" : ans
        })

    elif request.method == "POST":
        answer = bool(request.POST['answer'])
        try:
            if int(answer) == int(ans):
                message = "Correct"
            else : 
                message = "Incorrect"
            return JsonResponse({
                "state" : message
            })
        except: 
            return JsonResponse({
                "state": "incorrect response"
            })
    else:
        return HttpResponse("Invalid Request", 404)


def follow(request, username):
    pass
def following(request):
    pass
def profile(request,username):
    page_number = request.GET.get('page')
    user_obj = User.objects.get(username = username)
    user_stats = UserStats.objects.get(user = user_obj)
    return render(request, 'mathango/profile.html',{
        "user_obj" : user_obj,
        "user_stats" : user_stats
    })
def inbox(request, username):
    pass
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
            return render(request, "mathangoapp/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "mathangoapp/login.html")

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
            return render(request, "mathangoapp/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "mathangoapp/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "mathangoapp/register.html")
