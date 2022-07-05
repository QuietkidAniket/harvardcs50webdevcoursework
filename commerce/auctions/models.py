from django.contrib.auth.models import AbstractUser
from django.db import models as m
from django.util import timezone
class User(AbstractUser):
    pass

class Listing(m.Model):
   title = m.CharField(max_length=60)
   creation_date = m.DateTimeField(default = timezone.now) 
   #stores the exact time at which this listing would be created
   description = m.CharField(max_length= 500)
   startingBid = m.FloatField()
   currentBid = m.FloatField(blank = True, null= True)
   creator = m.Foreignkey(User, on_delete = m.CASCADE, related_name = "creators_list")
   spectators = m.ManytoManyField(User, blank = True, related_name = "spectators_list")
   buyer = m.Foreignkey(User, null = True,  on_delete = m.PROTECT)
   flactive = m.BooleanField(default=True)
   category = m.ManyToManyField(Category, related_name = "similar_listings")
   def __str__(self):
    return f"{self.title} | Starting Bid : {self.startingBid}, Current Bid : {self.currentBid}"

class Bid(m.Model):
    auction = m.ForeignKey(Listings, on_delete= m.CASCADE)
    user = m.ForeignKey(User, on_delete= m.CASCADE)
    offer = m.FloatField()
    date = m.DateTimeField(auto_now = True)
    #automatically updates the object to the current time
    
    def __str__(self):
        return f"{self.auction} : {self.user} offers {self.offer} ({self.date})"

class Comment(m.Model):
    comment = m.CharField(max_length = 200)
    creationdate = m.DateTimeField(default=timezone.now)
    user = m.ManyToManyField(User, on_delete=m.CASCADE, related_name ="user_comments")
    listing = m.ManyToManyField(Listing, on_delete= m.CASCADE, related_name = "listing_comments")
    def __str__(self):
        return f"{self.listing} | {self.comment} by {self.user} ({self.creationdate})"

class Category(m.Model):
    category = m.CharField(max_length=60)

    def __str__(self):
        return f" Category : {category}"