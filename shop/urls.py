from django.contrib import admin
from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.ProductListView.as_view(), name='product_list'),
    path('<int:product_id>/', views.ProductDetailView.as_view(), name = 'product_detail'),
    path('sundbox/', views.sundbox, name='sundbox'),
]
