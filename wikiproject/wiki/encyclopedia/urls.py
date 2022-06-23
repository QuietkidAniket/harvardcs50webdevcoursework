from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("edit<str:TITLE>",  views.edit, name = "edit"),
    path("random", views.randompage, name = "random"),
    path("search", views.search, name = "search"),
    path("newpage", views.newpage, name="newpage"),
    path("<str:TITLE>", views.entry, name="entry")
]