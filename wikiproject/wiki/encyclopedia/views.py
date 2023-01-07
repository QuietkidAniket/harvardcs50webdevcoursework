from django.shortcuts import render
from django.http import HttpResponse,  HttpResponseRedirect  
from . import util
from django.urls import reverse
from django import forms
import random

def index(request):
    """
    view for the home page (index path)
    """
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, TITLE):
    """
    view for the <TITLE> url (entry path)
    """
    entry = util.get_entry(TITLE)
    if entry == None:
        return HttpResponse("\t Requested Page was not Found!")
    l = list(entry)
    entry = ''.join(l)
    return render(request, "encyclopedia/entry.html", {
        "entry" : entry,
        "title" : TITLE
    })

def edit(request, TITLE):
    """
    view for the edit<TITLE> url (edit path)
    """
    if request.method == "POST":
        content = request.POST["content"]
        myfile = open(f".\\entries\\{TITLE}.md", "w")
        myfile.writelines(content.lstrip("<pre><code>"))
        myfile.close()
        return HttpResponseRedirect(f"{TITLE}") 
    return render(request, "encyclopedia/editpage.html",{
    "original" : util.get_entry(TITLE)
    })


def search(request):
    """
    search view for rendering the
    searchlist.html page (search url, search path)
    """
    title = request.POST["q"]
    return  render(request, "encyclopedia/searchlist.html", {
        "searchresult" : util.searchprocess(title)
    })
    
class newentry(forms.Form):
    """
    a class that inherits form.Form class of Django module,
    provids a template for the form
    """
    entryname = forms.CharField(label = "Entry Name ")
    entrytext =  forms.CharField(label= "Enter the content", widget=forms.Textarea(attrs={"rows":5, "cols":20}))

def newpage(request):
    """
    view for newpage url, path : newpage
    """
    if request.method == "POST":
        form = newentry(request.POST)
        if form.is_valid():
            pagename = form.cleaned_data["entryname"]
            if pagename not in util.list_entries():
                pagetext = form.cleaned_data["entrytext"]
                util.save_entry(title=pagename, content=pagetext)
                return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "encyclopedia/newpage.html", {
                "textarea": form
            })
    return render(request, "encyclopedia/newpage.html", {
        "textarea" : newentry()
    })

def randompage(request):
    """
    a view for displaying a random page, used for the url 'random', pathname : "random" 
    """
    l = util.list_entries()
    bound = len(l)
    random_index = random.randint(0,bound-1)
    randompage = l[random_index]
    return render(request, "encyclopedia/entry.html", {
        "entry" : util.get_entry(randompage),
        "title" : randompage
    })
