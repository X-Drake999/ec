from django.shortcuts import render, redirect
from django.views.generic import View, UpdateView
from cart.models import *
from shop.models import *
from .forms import *
from django.db.models import Avg, Count, Min, Sum, Prefetch
import datetime
import calendar
from dateutil.relativedelta import relativedelta
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse_lazy
import random

User = get_user_model()
def super_test_func(user):
    return user.is_superuser

@user_passes_test(super_test_func) 
def index(request):
    if not request.user.is_superuser:
        return redirect('shop:product_list')
    
    return render(request, 'staff/index.html', {})

@user_passes_test(super_test_func) 
def new(request):
    if not request.user.is_superuser:
        return redirect('shop:product_list')
    
    context = {'message': '', 'form': None}
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('shop:product_list')
        else:
            context['message'] = '再入力して下さい'
            context['form'] = form
    else:
        context['form'] = ProductForm()
    return render(request, 'staff/new.html', context)

class StatsView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_superuser
    
    def get(self, request, unit):
        
        if not request.user.is_superuser:
            return redirect('shop:product_list')
        
        d_today = datetime.date.today()
        d_month = d_today.month
        d_year = d_today.year
        
        if unit == 'week':
            purchased_carts = Cart.objects.filter(purchased=True).filter(purchased_date__gte= d_today.replace(day=1),
                                                                         purchased_date__lte = d_today)
            sales_list = purchased_carts.values('purchased_date').order_by('purchased_date').annotate(total_sale=Sum('total'))
            
        elif unit == 'year':
            purchased_carts = Cart.objects.filter(purchased=True).filter(purchased_date__gte= d_today - relativedelta(months=11) + 
                                                                         relativedelta(day=1), purchased_date__lte = d_today)
            sales_list = purchased_carts.values('purchased_date').order_by('purchased_date').annotate(total_sale=Sum('total'))

        sales_dict = {}

        if unit == 'week':
            start_day = d_today.replace(day=1)
            last_day = calendar.monthrange(d_year, d_month)[1]
            for i in range(last_day):
                td = datetime.timedelta(days=i)
                targeted_day = start_day + td
                sales_dict[targeted_day.strftime('%m月%d日')] = 0
            
            sales_dict = dict(sorted(sales_dict.items()))

        elif unit == 'year':                
            for i in reversed(range(12)):
                rd = relativedelta(months=i)
                past_month = d_today - rd
                sales_dict[past_month.strftime('%m月')] = 0
                
                
        if unit == 'week':
            message = '週間'
            for v in sales_list:
                if v['purchased_date'].strftime('%m月%d日') in sales_dict.keys() and v['purchased_date'].year == d_year:
                    sales_dict[v['purchased_date'].strftime('%m月%d日')] += v['total_sale']
        
        if unit == 'year':
            message = '年間'
            for v in sales_list:
                if v['purchased_date'].strftime('%m月') in sales_dict.keys():
                    sales_dict[v['purchased_date'].strftime('%m月')] += v['total_sale']
                    
        category_sales_for_pie = []
                    
        category_list = Category.objects.all()
        category_sales_dict = {}
        for category in category_list:
            category_sales_dict[category.name] = 0
        
        for targeted_cart in purchased_carts.prefetch_related(Prefetch("cartitem_set", queryset=CartItem.objects.all().select_related('product__category'), to_attr='cartitems')):#SELECT * from cart_item,product,categoryの結合, where cart_item.cart_id IN (purchased_cartsQuerySet内のcart.id全部)
            for targeted_cart_item in targeted_cart.cartitems: 
                category_sales_dict[targeted_cart_item.product.category.name] += targeted_cart_item.price * targeted_cart_item.quantity
        
        """
        改良前
         for targeted_cart in purchased_carts:
            for targeted_cart_item in targeted_cart.item_list():
                category_sales_dict[targeted_cart_item.product.category.name] += targeted_cart_item.item_total()
        """
                
        category_list = list(category_sales_dict.keys())
        category_sales = list(category_sales_dict.values())
        
        for sales, category in zip(category_sales, category_list):
            category_sales_for_pie.append({'value':sales, 'name':category})
            

        date = list(sales_dict.keys())
        sales = list(sales_dict.values())
        context = {'date':date, 'sales':sales, 'category_list':category_list, 'category_sales':category_sales, 'category_sales_for_pie': category_sales_for_pie, 'message':message}
        
        return render(request, 'staff/stats.html', context)

    
class TodayStatsView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_superuser
    
    def get(self, request):
        
        if not request.user.is_superuser:
            return redirect('shop:product_list')
        
        d_today = datetime.date.today()
        purchased_carts = Cart.objects.filter(purchased=True, purchased_date=d_today)
        
        if len(purchased_carts) == 0:
            context = {'sales': 0}
            return render(request, 'staff/today.html', context)
            
        sales_list = purchased_carts.values('purchased_date').order_by('purchased_date').annotate(total_sale=Sum('total'))
     
        date = [sales_list[0]['purchased_date'].strftime('%m月%d日')]
        total_sales = [sales_list[0]['total_sale']]
        
        category_list = Category.objects.all()
        category_sales_dict = {}
        for category in category_list:
            category_sales_dict[category.name] = 0
        
        for targeted_cart in purchased_carts:
            for targeted_cart_item in targeted_cart.item_list().select_related('product', 'product__category'):#cart_item,product,categoryの結合
                category_sales_dict[targeted_cart_item.product.category.name] += targeted_cart_item.item_total()
        

        category_list = list(category_sales_dict.keys())
        category_sales = list(category_sales_dict.values())
        
        sales_str = str(total_sales[0])
        
        
        context = {'date':date, 'sales':total_sales, 'sales_str':sales_str, 'category_list':category_list, 'category_sales':category_sales}
        
        return render(request, 'staff/today.html', context)

@user_passes_test(super_test_func) 
def edit_index(request):
    if not request.user.is_superuser:
        return redirect('shop:product_list')
    
    products = Product.objects.all()
    
    context = {'products':products}
    
    return render(request, 'staff/edit_index.html', context)
        
class ProductUpdateView(UserPassesTestMixin, UpdateView): 
    def test_func(self):
        return self.request.user.is_superuser

    model = Product
    fields = ('name', 'image', 'description', 'category', 'price', 'stock', 'available', )
    template_name = 'staff/edit_product.html'
    success_url = reverse_lazy('staff:edit_index')

    
class UnavailableProductView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_superuser
    
    def get(self, request):
        form = ProductSelectForm()
        return render(request, 'staff/unavailable.html', {'form':form})
    
    def post(self, request):
        form = ProductSelectForm(request.POST)
        context = {'form':form}
        if form.is_valid():
            picked = form.cleaned_data.get('picked')  #pickedにはstrで入ってしまう, ModelObjectのままほしい
            context['message'] = '変更に成功しました'
            
            for pick in picked:
                product = Product.objects.get(name=pick)
                product.available = False
                product.save()
            
            return render(request, 'staff/unavailable.html', context)
        
        else:
            context['message'] = '変更に失敗しました'
            return render(request, 'staff/unavailable.html', context)
        
def add_purchase_log(request):
    
    if 'num' in request.GET:
        num = int(request.GET['num'])
        
        if num < 1 or 1000 < num:
            return render(request, 'staff/index.html', {})
        
    else:
        return render(request, 'staff/index.html', {})
    
    for _ in range(num):    
        cart = Cart()
        cart.user = random.choice(User.objects.all())
        cart.purchased = True

        td = datetime.timedelta(days=random.randrange(31))
        cart.purchased_date = datetime.date.today() - td

        cartitem = CartItem()
        cartitem.product = random.choice(Product.objects.all())
        cartitem.cart = cart
        cartitem.quantity = random.randrange(1, 3)
        cartitem.price = cartitem.product.price
        cart.save()
        cartitem.save()

        cart.total = cart.cart_total()

        cart.save()
    
    return render(request, 'staff/index.html', {})
    
    
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        

