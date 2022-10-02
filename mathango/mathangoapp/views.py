from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import User, UserStats, Game, Follow, Message
import random

# Create your views here.

def index(request):
    if request.user.is_authenticated:
        reload(request)
        return render(request, "mathangoapp/index.html")
    else:
        return HttpResponseRedirect("login")


def creategame(request):
    if request.method == 'GET':
        
        time = int(request.GET.get('time'))
        
        return render(request, "mathangoapp/game.html", {
            "customtime" : time,
            
        })

    else:
        return HttpResponse("Invalid Request", 404)
        
def search(request):
    username= request.POST["search-query"]
    profile(request, username)

def leaderboard(request):
    reload(request)
    pass

def game(request):
    if request.method == "GET":
        
        
        if request.GET.get('state') == 'get':       
        
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
                    
                    
        elif request.GET.get('state') == 'put':    
            answer = int(request.GET.get('answer'))
            ans = int(request.GET.get('correctans'))
            try:
                if answer == ans:
                    message = "Correct"
                else : 
                    message = "Incorrect"
                return JsonResponse({
                    "state" : message
                })
            except: 
                return JsonResponse({
                    "state": "Incorrect"
                })       
    else:
        return HttpResponse("Invalid Request", 404)

def reload(request):
    user = request.user 
    if user.is_authenticated :
        userstatobj = None
        games = None
        try:
            #exception
            userstatobj = UserStats.objects.get(user = user)
        except: 
            userstatobj = UserStats(user=user, avg_response_time=0.0 , total_right=0)
        #exception
        try:
            games = list(user.games_played.all())
        except:
            games = []
        if len(games) !=0 :
            avg_response_time = 0.0
            total_wrong = 0
            total_right = 0
            rw = 0.0
            counter = 0.0
            for game in games:
                counter = counter+ float(game.avgresponsetime)
                total_right = total_right + game.right
            avg_response_time = float(counter/ len(games))
            print(avg_response_time)
            userstatobj.user=user
            userstatobj.avg_response_time = float(avg_response_time) 
            userstatobj.total_right = total_right  
            userstatobj.save()
            
        
        else:   
            userstatobj = UserStats(user=user, avg_response_time = 0.0 , total_right = 0) 
            userstatobj.save()
    

def endgame(request, noofquestions, time):
    #creating a new game
    obj = Game(player = request.user, right = noofquestions, totalresponsetime=time, avgresponsetime= float(time/noofquestions))
    obj.save()
    reload(request)
    

def follow(request, username):
    user =  User.objects.get(username = username)
    try:
        obj = Follow.objects.get(user = request.user, following = user)
        obj.delete()
    except:
        follow_obj = Follow(user = request.user, following = user)
        follow_obj.save() 
        return HttpResponseRedirect(reverse(f"/profiles/{username}?page=1"))


def profile(request,username):
    page_number = request.GET.get('page')
    user = User.objects.get(username = username)
    user_stats = UserStats.objects.get(user = user)
    username = user.username
    avgresponsetime = user_stats.avg_response_time
    totalright = user_stats.total_right
    user_himself = False
    is_following = False

    #if the requesting user is the user himself
    if user == request.user :
        user_himself = True   
    else : 
        try :
            obj = Follow.objects.get(user = request.user, following = user)
            is_following = True
        except: 
            is_following = False

    following_users = list()
    objs = list()
    temp_objs = list()
    all_objs = list(reversed(Message.objects.all()))

    
        
        
    try:
        for following in Follow.objects.filter(user = request.user).all():
            following_users.append(following.following)
        print(following_users)
        for user in following_users:
            temp_objs.extend(user.posts.all())
        for obj in all_objs:
            if obj in temp_objs:
                objs.append(obj)

    except: 
        print("no such objects")

    """sending pages"""
    p =  Paginator(objs, 10) 
    #by default 1st page is sent
    page_obj = p.page(1)
    page_number =  1
    #if a get request asks for a page, that page is stored in page_obj
    if request.method == "GET":
                    
            page_number = request.GET.get('page')
            page_obj = p.page(page_number)
    # sending the number of followers and following
    nooffollowers = len(list(user.followers_list.all()))
    nooffollowing = len(list(user.following_list.all()))
    return render(request, 'mathangoapp/profile.html',{
        "username":username,
        "user_himself":user_himself,
        "totalright":totalright,
        "is_following" : is_following,
        "avgresponsetime":avgresponsetime,
        "is_following" : is_following,
        "nooffollowers":nooffollowers,
        "nooffollowing":nooffollowing,
        "page_obj":page_obj,
        "page_number":page_number
    })


def inbox(request):
    content = request.POST['content']
    obj = Message(creator=request.user, content=content)
    obj.save()
    
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
