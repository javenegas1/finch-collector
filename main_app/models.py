from django.db import models

# Create your models here.

class Car(models.Model):

    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    image = models.CharField(max_length=250)
    bio = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.make

    class Meta:
        ordering = ['make']