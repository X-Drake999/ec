from django.contrib import admin
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('<int:pk>/', views.ProfileView.as_view(), name = 'profile'),
    path('add/', views.new, name = 'add'),
    path('edit/<int:pk>', views.UserUpdateView.as_view(), name = 'edit'),
    path('edit/password/<int:pk>', views.PasswordUpdateView.as_view(), name = 'password_edit'),
    path('login/', views.LoginView.as_view(), name = 'login'),
    path('logout/', views.LogoutView.as_view(), name = 'logout'),
]
