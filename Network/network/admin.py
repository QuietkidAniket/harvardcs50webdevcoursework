from django.contrib import admin
from .models import User, Post, Follow
# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "password")
class PostAdmin(admin.ModelAdmin):
    list_display = ("id","creator","title", "date",)

class FollowAdmin(admin.ModelAdmin):
    list_display = ("id","user")
admin.site.register(User, UserAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Follow, FollowAdmin)