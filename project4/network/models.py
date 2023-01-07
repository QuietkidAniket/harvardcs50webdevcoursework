from django.contrib.auth.models import AbstractUser
from django.db import models as m
from django.utils import timezone

class User(AbstractUser):
    pass

class Post(m.Model):
    creator = m.ForeignKey(User, on_delete= m.CASCADE, related_name = "posts")
    title = m.CharField(max_length=200)
    content = m.CharField(max_length=3000)
    date = m.DateTimeField(default = timezone.now)
    like = m.ManyToManyField(User, blank = True, related_name = "likes_by_user")
    dislike = m.ManyToManyField(User, blank = True, related_name = "dislikes_by_user")
    nooflikes = m.IntegerField(default = 0)
    noofdislikes = m.IntegerField(default = 0)


class Follow(m.Model):
    user = m.ForeignKey(User, on_delete = m.CASCADE, related_name="following_list")
    following = m.ForeignKey(User, blank = True, on_delete = m.CASCADE, related_name = "followers_list")
