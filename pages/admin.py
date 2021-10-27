from django.contrib import admin

from .models import Client, Favourite, Offer, Order, Section, Product

# Register your models here.

admin.site.register(Section)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Offer)
admin.site.register(Favourite)
admin.site.register(Client)
