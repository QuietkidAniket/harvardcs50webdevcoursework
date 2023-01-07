from django.urls import path
from . import views
urlpatterns=[
    path("", views.index, name="index"),
    path("creategame", views.creategame, name="creategame"),
    path("game", views.game, name="game"),
    path("endgame/<int:noofquestions>/<int:time>", views.endgame, name="endgame"),
    path("profiles/<str:username>", views.profile, name="profile"),
    path("search", views.search, name="search"),
    path("inbox", views.inbox, name="inbox"),
    path("leaderboard", views.leaderboard, name="leaderboard"),
    path("follow/<str:username>", views.follow, name="follow"),
    path("invalid",views.invalid,name="invalid"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]