from django.contrib import admin
from .models import User, Listing, Comment, Bid, Category, Picture
# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ["username","email","password"]
class ListingAdmin(admin.ModelAdmin):
    list_display = ["title", "creator", "description", "startingBid", "currentBid","buyer", "category","flactive"]
class BidAdmin(admin.ModelAdmin):
    list_display = ["auction", "user", "offer", "date"]
class CommentAdmin(admin.ModelAdmin):
    list_display = ["comment","user", "listing"]
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["category"]
class PictureAdmin(admin.ModelAdmin):
    list_display = ["listing","image","alt_text"]
admin.site.register(User,UserAdmin)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Picture, PictureAdmin)
