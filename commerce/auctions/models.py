from email.policy import default
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Category(models.Model):
    categoryName = models.CharField(max_length=500)
    def __str__(self):
        return f"{ self.categoryName }"

class Bid(models.Model):
    bid = models.FloatField(default=0)
    user = models.ForeignKey(User, on_delete = models.CASCADE, null=True, related_name = "bidUser")

    def __str__(self):
        return f"{ self.bid }"    

class Listing(models.Model):
    title = models.CharField(max_length = 50)
    description = models.CharField(max_length = 500)
    imageUrl = models.CharField(max_length = 2000)
    price = models.ForeignKey(Bid, on_delete = models.CASCADE, blank=True, null=True, related_name="bidPrice")
    isActive = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete = models.CASCADE, null=True, related_name = "user")
    category = models.ForeignKey(Category, on_delete = models.CASCADE, related_name="category")
    watchlist = models.ManyToManyField(User, blank=True, null=True, related_name="Watchlisting")

    def __str__(self):
        return f"{ self.title } - { self.price}" 

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete = models.CASCADE, null=True, related_name = "commentUser")
    listing = models.ForeignKey(Listing, on_delete = models.CASCADE, null=True, related_name = "listingComment")
    comment = models.CharField(max_length = 500)

    def __str__(self):
        return f"{ self.author } comment on { self.listing }" 


