from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Car(models.Model):

    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    image = models.CharField(max_length=250)
    bio = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    
    def __str__(self):
        return self.make

    class Meta:
        ordering = ['make']

class Sale(models.Model):

    owner = models.CharField(max_length=150)
    price = models.IntegerField(default=1)
    make = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="sales")

    def __str__(self):
        return self.owner

class Wishlist(models.Model):

    title = models.CharField(max_length=70)
    # this is going to create the many to many relationship and join table
    cars = models.ManyToManyField(Sale)

    def __str__(self):
        return self.title