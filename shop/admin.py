from django.contrib import admin
from .models import Product, Category, ProductLog
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'stock', 'available']
    list_editable = ['category', 'price', 'stock', 'available']
admin.site.register(Product, ProductAdmin)

admin.site.register(Category)
admin.site.register(ProductLog)