from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import *


# Register your models here.
class ListingsAdmin(admin.ModelAdmin):
    list_display = ("id",
                    "title",
                    "description",
                    "start_price",
                    "category",
                    "image",
                    "date",
                    "user",
                    "closed",
                    "winner")


class WatchListAdmin(admin.ModelAdmin):
    list_display = ("user_id", "item_id")


class CommentsAdmin(admin.ModelAdmin):
    list_display = ("text", "user_id", "item_id")


class BidAdmin(admin.ModelAdmin):
    list_display = ("amount", "user_id", "item_id")


admin.site.register(User, UserAdmin)
admin.site.register(Listings, ListingsAdmin)
admin.site.register(WatchList, WatchListAdmin)
admin.site.register(Comments, CommentsAdmin)
admin.site.register(Bid, BidAdmin)

