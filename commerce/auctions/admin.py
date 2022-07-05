from django.contrib import admin
from .models import User, Listing, Comment, Bid, Category
# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ("username","email","password")
class ListingAdmin(admin.ModelAdmin):
    list_display = ("title", "listing", "creator", "description", "startingBid", "currentBid","category","buyer","spectators", "flactive")
class BidAdmin(admin.ModelAdmin):
    list_display = ("auction", "user", "offer", "date")
class CommentAdmin(admin.ModelAdmin):
    list_display = ("comment","creation_date","user", "listing")
class CategoryAdmin(admin.ModelAdmin):
    list_display("category")
admin.site.register(User,UserAdmin)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Category, CategoryAdmin)
