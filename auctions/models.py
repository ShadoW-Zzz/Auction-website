from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class category(models.Model):
    categoryName = models.CharField(max_length=20)

    def __str__(self):
        return self.categoryName
    
    class Meta:
        verbose_name = 'Category'  
        verbose_name_plural = 'Categories'

class Bid(models.Model):
    bid_amt = models.IntegerField()
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_bid")
    bid_count = models.IntegerField(null=True, blank=True)
    initial_bid = models.IntegerField() 

    def __str__(self):
        return str(self.bid)

class listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=250)
    price = models.ForeignKey(Bid, on_delete=models.CASCADE, related_name="bid")
    img_url = models.CharField(max_length=1000)
    status = models.BooleanField(default=True)
    publisher = models.ForeignKey(User , on_delete=models.CASCADE, related_name="user", null=True , blank=True)
    category = models.ForeignKey(category,  on_delete=models.CASCADE, related_name = "Games")
    watchlist = models.ManyToManyField(User, null=True, blank=True, related_name="intrested_watchlist")

    def __str__(self):
        return self.title


class comments(models.Model):
    comment = models.CharField(max_length=500)
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="usercomments")
    comment_listing = models.ForeignKey(listing , on_delete=models.CASCADE, related_name="listingcomments")

    def __str__(self):
        return f"Comment by {self.comment_user}: {self.comment[:20]}"
