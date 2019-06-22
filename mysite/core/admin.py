from django.contrib import admin
from .models import Products
from .models import Subscribers
# Register your models here.

class ProductsAdmin(admin.ModelAdmin):
      list_display    = ['name']
	  
class SubscribersAdmin(admin.ModelAdmin):
    list_display = ('user', 'subscriptions')

admin.site.register(Products, ProductsAdmin)
admin.site.register(Subscribers, SubscribersAdmin)