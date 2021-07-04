from django.contrib import admin
from .models import *
# Register your models here.

class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'purchased', 'purchased_date', 'total']
    list_editable = ['purchased', 'purchased_date']
admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem)