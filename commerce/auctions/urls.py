from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("watchlist", views.watchlist, name = "watchlist"),
    path("categories", views.categories, name="categories"),
    path("addtowatchlist/<int:id>", views.addtowatchlist, name = "addtowatchlist"),
    path("removefromwatchlist/<int:id>",views.removefromwatchlist, name = "removefromwatchlist"),
    path("close/<int:id>", views.closeauction, name = "closeauction"),
    path("bid/<int:id>", views.bid, name = "bid"),
    path("comment/<int:id>", views.comment,  name="comment"),
    path("add", views.newlisting, name = "newlisting"),
    path("category/<str:category_name>", views.categorylistings, name = "categorylistings"),
    path("listing/<int:id>", views.listing, name= "listing")
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
