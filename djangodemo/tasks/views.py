from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
tasklist=[]
class NewTaskForm(forms.Form): # our NewTaskForm inherits from Form which is present in froms module
    task = forms.CharField(label= "New Task")
    priority = forms.IntegerField(label="Priority", min_value= 1, max_value =10)

# Create your views here.
def index(request):
    if "tasklist" not in request.session:
        request.session["tasklist"] = []
    return render(request, "tasks/index.html", { "tasks" : request.session["tasklist"]
    }) 
#{"html template variable which django will try to access" , python variable }

# Add a new task:
def add(request):
    #check whether the method is post
    if request.method == "POST":
        #take in the data user submitted and save it as a form
        form = NewTaskForm(request.POST)
        #check if the form is valid (server-side)
        if form.is_valid():
            #isolate the task from the cleaned version of the form data
            task = form.cleaned_data["task"]
            #add a new task to our task list
            request.session["tasklist"] += [task]
            #Redirect the user to the list of tasks
            return(HttpResponseRedirect(reverse("tasks:index")))
        else:
            #if the form is invalid, then rerender the page with existing information
            return render(request, "tasks/add.html", { "form" : form}) #(a html template variable, python variable)
    else:
        return render(request, "tasks/add.html", {"form": NewTaskForm()})