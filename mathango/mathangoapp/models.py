from django.contrib.auth.models import AbstractUser
from django.db import models as m
from django.utils import timezone

    
# Create your models here.
class User(AbstractUser):
    pass

class UserStats(m.Model):
    user = m.ForeignKey(User, on_delete=m.CASCADE, related_name="stats")
    avg_response_time = m.FloatField(default=0)
    total_right = m.IntegerField(default=0)
    total_wrong = m.IntegerField(default=0)
    rw = m.IntegerField(default=0)

class Game(m.Model):
    player = m.ForeignKey(User, on_delete=m.CASCADE, related_name="games_played")
    questions = m.IntegerField(default=0)
    right = m.IntegerField(default=0)
    difficulty = m.IntegerField(default=1)
    avg_response_time= m.FloatField(default=0.0)
    total_response_time= m.FloatField(default=0.0)    

class Follow(m.Model):
    user = m.ForeignKey(User, on_delete = m.CASCADE, related_name="following_list")
    following = m.ForeignKey(User, blank = True, on_delete = m.CASCADE, related_name = "followers_list")

class Post(m.Model):
    game = m.ForeignKey(Game, on_delete= m.CASCADE, related_name="related_posts")
    creator = m.ForeignKey(User, on_delete= m.CASCADE, related_name = "posts")
    content = m.CharField(max_length=3000)
    date = m.DateField(default = timezone.now)
    
