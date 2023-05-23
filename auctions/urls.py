from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("listings/<int:index>", views.listing, name="listing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("addToWatchlist/<int:index>", views.watchlist_add, name="addToWatchlist"),
    path("removeFromListing/<int:index>", views.listing_watchlist_remove, name="removeFromListing"),
    path("removeFromWatchlist/<int:index>", views.watchlistpage_watchlist_remove, name = "removeFromWatchlist"),
    path("bid/<int:index>", views.bid, name="bid"),
    path("close/<int:index>", views.close, name = "close"),
    path("comment/<int:index>", views.comment, name = "comment"),
    path("categories", views.categories, name = "categories"),
    path("categories/<int:index>", views.categories_search, name = "categories_search")
]
