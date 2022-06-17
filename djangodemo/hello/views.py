from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
# request - http request

def brian(request):
    return HttpResponse("Hello Brian")
def david(request):
    return HttpResponse("Hello David")
def greet(request, name):
    return render(request, "hello/greet.html", {
        "username" : name.capitalize()  
    })
def index(request):
    return render(request, "hello/index.html")