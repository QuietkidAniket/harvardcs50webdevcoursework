from django.urls import path
from . import views

app_name = "tasks"  #helps to uniquely identify urls , avoids mamespace collision
urlpatterns = [
    path("add", views.add, name="add"),
    path("", views.index, name="index")   
]