from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import User, Post, Follow

from django.core.paginator import Paginator

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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")

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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def index(request):
    if not request.user.is_authenticated:
        return render(request, "network/login.html")
    if request.method == 'POST': 
        body = request.POST['body']
        title = request.POST.get("title")
        user = request.user
        post_obj = Post(creator = user, content = str(body), title = str(title))
        post_obj.save()
        return HttpResponseRedirect(reverse("index"))
    
    
        

    #all recent posts
    objs =  list(reversed(Post.objects.all()))
       

    """sending pages"""
    p =  Paginator(objs, 10) 
    print(len(objs))
    #by default 1st page is sent
    page_obj = p.page(1)
    page_number =  1
    #if a get request asks for a page, that page is stored in page_obj
    if request.method == "GET":
            page_number = request.GET.get('page')
            if page_number == None:
                page_number =1
            page_obj = p.page(page_number)
        
    
    return render(request, 'network/index.html', {
        "pages" : p,
        "page_number" : page_number,
        "noofpages" : p.num_pages,
        "page_obj" : page_obj,
    })
    
@login_required
def profile(request, username):

    if request.user.is_authenticated :
        user = User.objects.get(username = username)

        #posts of user
        objs =  list(reversed(Post.objects.filter(creator =  user)))

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
        
        return render(request, 'network/profilepage.html', {
            "username" : username, 
            "user_himself" : user_himself,
            "pages" : p,
            "page_number" : page_number,
            "noofpages" : p.num_pages,
            "page_obj" : page_obj,
            "nooffollowers" : nooffollowers,
            "nooffollowing" : nooffollowing,
            "is_following" : is_following
        })
    else:
        return render(request, 'network/login.html')
@login_required()
def showfollowedposts(request):
    following_users = list()
    objs = list()
    temp_objs = list()
    all_objs = list(reversed(Post.objects.all()))
    try:
        for following in Follow.objects.filter(user = request.user).all():
            following_users.append(following.following)
        print(following_users)
        for user in following_users:
            print(user)
            print(user.posts.all())
            temp_objs.extend(user.posts.all())
        for obj in all_objs:
            if obj in temp_objs:
                objs.append(obj)
    except: 
        print("no such objects")
    finally:    
        p =  Paginator(objs, 10) 
        print(len(objs))
        #by default 1st page is sent
        page_obj = p.page(1)
        page_number =  1
        #if a get request asks for a page, that page is stored in page_obj
        if request.method == "GET":
                page_number = request.GET.get('page')
                if page_number == None:
                    page_number =1
                page_obj = p.page(page_number)
        return render(request, 'network/followposts.html', {
            "pages" : p,
            "page_number" : page_number,
            "noofpages" : p.num_pages,
            "page_obj" : page_obj,
        })
@login_required
def follow(request, username):
    user =  User.objects.get(username = username)
    try:
        obj = Follow.objects.get(user = request.user, following = user)
        obj.delete()
    except:
        follow_obj = Follow(user = request.user, following = user)
        follow_obj.save() 
        return HttpResponseRedirect(reverse(f"/profiles/{username}?page=1"))

@login_required
def setlikes(request):
    post_id = int(request.GET.get('post_id'))
    post = Post.objects.get(pk = post_id)
    if request.user in post.like.all():
        post.like.remove(request.user.id)
        
    else :
        post.like.add(request.user)
    post.nooflikes = len(post.like.all())
    post.save()
    nooflikes = post.nooflikes
    return JsonResponse({
        "nooflikes" : str(nooflikes)
    })
@login_required
def setdislikes(request):
    post_id = int(request.GET.get('post_id'))
    post = Post.objects.get(pk = post_id)
    if request.user in post.dislike.all():
        post.dislike.remove(request.user.id)
    else :
        post.dislike.add(request.user)
    post.noofdislikes = len(post.dislike.all())    
    post.save()
    noofdislikes = post.noofdislikes
    return JsonResponse({
        "noofdislikes" : str(noofdislikes)
    })
@login_required
def edit(request, post_id):
    
    post = Post.objects.get(pk = post_id)
    if(request.user != post.creator):
        return HttpResponse("Invalid Address!")
    if  request.method == "POST":

        title = request.POST['title']
        content = request.POST['body']
        post.title = title
        post.content = content
        post.save()
        return HttpResponseRedirect(f"/profiles/{request.user.username}?page=1")


    return render(request, 'network/editpost.html', {
        "post": post
    })

    