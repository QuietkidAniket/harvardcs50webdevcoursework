from django.urls import path
#from current directory import views.py module
from . import views
 #list of all allowed url that would be used by this app
urlpatterns = [
    path("brian", views.brian, name = "brian" ),#another route that loads brian function
    path("david", views.david, name = "david"), #another route that loads david functiion
    path("",views.index, name = "index"),#("" -> specfies default url which loads when 
                                        #the user uses the default route to view the app
                                        #, views.index function, name to the path)
    path("<str:name>", views.greet, name = "greet") #<str:name> refers to the name argument
                                                    #which views.greet() function receives from here.
]   