from django.contrib import admin
from django.urls import path
from . import views

app_name = 'staff'

urlpatterns = [
    path('', views.index, name='index'),
    path('edit/<int:pk>/', views.ProductUpdateView.as_view(), name='edit_product'),
    path('edit/', views.edit_index, name='edit_index'),
    path('stats/today/', views.TodayStatsView.as_view(), name='today'),
    path('stats/<str:unit>/', views.StatsView.as_view(), name='stats'),
    path('new/', views.new, name='new'),
    path('unavailable/', views.UnavailableProductView.as_view(), name='unavailable'),
]
