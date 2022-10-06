from django.contrib import admin
from .models import Car, Sale, Wishlist

# Register your models here.

admin.site.register(Car)
admin.site.register(Sale)
admin.site.register(Wishlist)