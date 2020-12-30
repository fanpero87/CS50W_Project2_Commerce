from django.urls import path

from . import views

urlpatterns = [
    path("index", views.index, name="index"),
    path("", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add", views.add_item, name="add"),
    path("item/<int:item_id>", views.listing_page, name="item"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("add_watchlist", views.add_watchlist, name="add_watchlist"),
    path("remove_watchlist", views.remove_watchlist, name="remove_watchlist"),
    path("add_bid", views.add_bid, name="add_bid"),
    path("add_comment", views.add_comment, name="add_comment"),
    path("close_listing", views.close_listing, name="close_listing"),
    path("closed_listings", views.all_closed_listings, name="closed_listings"),
    path("categories", views.categories, name="categories"),
    path("category/<str:name>", views.category_page, name="category")
]
