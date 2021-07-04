from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View
from .models import *
from django.db.models import Q

# Create your views here.
class ProductListView(View):
    def get(self, request):
        if 'category' in request.GET:
            products = Product.objects.filter(category__name=request.GET['category'], available=True)
            category_name = "カテゴリー: {} の ".format(request.GET['category'])
        
        elif 'q' in request.GET:
            query = request.GET['q']
            products = Product.objects.all().filter(Q(name__contains=query), available=True) #  | Q(description__contains=query)
            category_name = "「{}」の ".format(query)
            
        else:
            products = Product.objects.filter(available=True)
            category_name = 'すべての '
            
        context = {
            'products': products,
            'categories': Category.objects.all(),
            'category_name': category_name,
        }
        return render(request, 'shop/product_list.html', context)
    
class ProductDetailView(View):
    def get(self, request, product_id):
        product = get_object_or_404(Product, pk = product_id)
        return render(request, 'shop/product_detail.html', {'product':product})


def sundbox(request):
    context = {'list':[85, 20, 36, 10, 10, 20]}
    return render(request, 'shop/sundbox.html', context)