from django.contrib.auth.models import AbstractUser
from django.db import models

CATEGORY_CHOICES = (
    ('Art', 'Art'),
    ('Cars', 'Cars'),
    ('Cloths', 'Cloths'),
    ('Electronics', 'Electronics'),
    ('Fashion', 'Fashion'),
    ('Manuscript', 'Manuscript'),
    ('Toys', 'Toys')
)


# Create your Models here
class User(AbstractUser):
    pass


class Listings(models.Model):
    objects = None
    title = models.CharField(max_length=64)
    description = models.TextField(blank=True, null=True)
    start_price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=15)
    image = models.ImageField(blank=True)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    closed = models.BooleanField(default=False)
    winner = models.TextField(blank=True, null=True)


class WatchList(models.Model):
    objects = None
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    item_id = models.ForeignKey(Listings, on_delete=models.CASCADE)


class Comments(models.Model):
    objects = None
    text = models.TextField(max_length=200)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    item_id = models.ForeignKey(Listings, on_delete=models.CASCADE)


class Bid(models.Model):
    objects = None
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    item_id = models.ForeignKey(Listings, on_delete=models.CASCADE)