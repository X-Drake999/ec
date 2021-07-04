from django.db import models
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from shop.models import *

User = get_user_model()
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    purchased = models.BooleanField(default=False)
    purchased_date = models.DateField(null=True, blank=True)
    total = models.IntegerField(null=False, blank=False, default=0)
    
    def __str__(self):
        return "{}'s cart".format(self.user.username)
    
    def item_list(self):
        item_list = CartItem.objects.filter(cart=self)# インスタンスとしての自らを使用
        return item_list
    
    def cart_total(self):
        item_list = self.item_list()
        total = 0
        for item in item_list:
            total += item.item_total()
            
        return total
       
    
class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.IntegerField(null=True, blank=True)
    
    def item_total(self):
        if self.price:
            return self.price * self.quantity
        elif self.price == None:
            return self.product.price * self.quantity
    
    def __str__(self):
        return self.product.name

    
    