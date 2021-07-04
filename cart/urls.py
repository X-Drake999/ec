from django.contrib import admin
from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.CartDetailView.as_view(), name = 'detail'),
    path('add/<int:product_id>/', views.add_cart, name = 'add'),
    path('remove/<int:product_id>/', views.cart_remove, name = 'remove'),
    path('full_remove/<int:product_id>/', views.full_remove, name = 'full_remove'),
    path('log/', views.PurchaseLog.as_view(), name = 'log'),
    path('confirm_purchase/<int:cart_id>', views.confirm_purchase, name = 'confirm'),
]