from django.contrib.auth.models import AbstractUser
from django.db import models
from .choices import *
from django.utils import timezone


class User(AbstractUser):
    pass


class Listings(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    category = models.IntegerField(choices=CATEGORY_CHOICE, default=0)
    description = models.TextField()
    url = models.URLField(default=None)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    closed = models.BooleanField(default=False)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"name: {self.name} price:{self.price} "


class Bids(models.Model):
    starting_bid = models.DecimalField(decimal_places=2, max_digits=10)
    user_bid = models.DecimalField(
        decimal_places=2, max_digits=10, default=None)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bid_listing = models.ForeignKey(
        Listings, on_delete=models.CASCADE, related_name="bid")


class Comments(models.Model):
    id = models.AutoField(primary_key=True)
    comment_section = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_listing = models.ForeignKey(
        Listings, on_delete=models.CASCADE, related_name="comment")
    


class WatchList(models.Model):
    watchlist_item = models.ForeignKey(Listings, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="my_watchlist")

