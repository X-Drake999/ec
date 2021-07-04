from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth import get_user_model
from .models import *
from django.urls import reverse
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator

User = get_user_model()
class CartDetailView(View):
    def get(self, request):
        try:
            cart = Cart.objects.get(user=request.user, purchased=False)
            
        except ObjectDoesNotExist:
            if request.user.is_anonymous:
                return HttpResponseRedirect(reverse('accounts:login')) #reverseだけじゃダメ？HttpResponseRedirectで通るように               
            else:
                cart = Cart.objects.create(user=request.user) #Cartオブジェクトのuserがnot nullなので指定が必要だった
                
        cart_items = CartItem.objects.filter(cart=cart)
        total = cart.cart_total()

        return render(request, 'cart/cart_detail.html', {'cart':cart, 'cart_items':cart_items, 'total':total})
    
class PurchaseLog(View):
    def get(self, request):
        if Cart.objects.filter(user=request.user, purchased=True).exists() == True:
            message = 'さんの購入履歴'
            context = {'cart_list':[], 'message':message}
            
            purchased_carts_lists = Cart.objects.filter(user=request.user, purchased=True).order_by('-purchased_date')
            paginator = Paginator(purchased_carts_lists, 3)
            p = request.GET.get('p')
            targeted_carts_lists = paginator.get_page(p)
            
            for cart in targeted_carts_lists:
                
                date = cart.purchased_date
                item_list = cart.item_list

                cart_info = [date, item_list]
                context['cart_list'].append(cart_info)
                
            context['targeted_carts_lists'] = targeted_carts_lists 
                
            return render(request, 'cart/log.html', context)
                    
        else:
            return redirect('cart:detail')
            
            
def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user, purchased=False)  
    
    cart_item, created = CartItem.objects.get_or_create(product=product, cart=cart, defaults=dict(quantity=0))
    cart_item.quantity += 1
    cart_item.save()
      
    return redirect('cart:detail')
        
def cart_remove(request, product_id):
    product = Product.objects.get(id=product_id)
    cart = Cart.objects.get(user=request.user, purchased=False)   
    cart_item = CartItem.objects.get(product=product, cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()      
    return redirect('cart:detail')

def full_remove(request, product_id):
    product = Product.objects.get(id=product_id)
    cart = Cart.objects.get(user=request.user, purchased=False)   
    cart_item = CartItem.objects.get(product=product, cart=cart)
    cart_item.delete()
    return redirect('cart:detail')

def confirm_purchase(request, cart_id):
    cart = Cart.objects.get(id=cart_id)  
    cart.purchased = True
    cart.purchased_date = timezone.datetime.today()
    cart.total = cart.cart_total()
    cart.save()
    
    cart_items = cart.item_list()
    for cart_item in cart_items:
        cart_item.price = cart_item.product.price
        cart_item.save()
    return redirect('cart:log')
    
    
    
    
    
    
        
    