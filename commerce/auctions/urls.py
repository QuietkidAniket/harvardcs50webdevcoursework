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
    path("<str:category_name>", views.categorylistings, name = "categorylistings"),
    path("listing/<str:title>", views.listing, name= "listing")
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
