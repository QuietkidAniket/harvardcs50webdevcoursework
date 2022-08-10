from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
# Create your views here.
def index(request):
    return render(request,"singlepage/index.html")

texts = ["This is the first text","This is the second text", "This is the third text"]

def sections(request, num):
    if 1<= num <= 3:
        return HttpResponse(texts[num -1])
    else:
        return Http404('sections not found')