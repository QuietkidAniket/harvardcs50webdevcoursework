
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("setlike", views.setlikes, name="setlike"),
    path("setdislike" ,views.setdislikes, name = "setdislike"),
    path("edit/<int:post_id>" ,views.edit, name = "edit"),
    path("follow/<str:username>", views.follow, name="follow"),
    path("profiles/<str:username>", views.profile , name = "profile"),
    path("followedposts", views.showfollowedposts, name = "showfollowedposts"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]
