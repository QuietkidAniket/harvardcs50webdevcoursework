from django.contrib import admin
from .models import User, UserStats, Game, Follow, Post
# Register your models here.
admin.site.register(User)
admin.site.register(UserStats)
admin.site.register(Game)
admin.site.register(Follow)
admin.site.register(Post)
