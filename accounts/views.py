from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.views import LoginView as AuthLoginView
from django.contrib.auth.views import LogoutView as AuthLogoutView
from django.views.generic import UpdateView, DetailView, View
from django.urls import reverse_lazy
from .models import *
from .forms import *

#UserCreationFormの継承で通るようになった
#defaultのUserCreationFormはAuth.Userしか使えない？

User = get_user_model()

class ProfileView(DetailView):
    template_name = 'accounts/profile.html'
    model = User
    #queryset = User.objects.all()

def new(request, user_id=None):
    if user_id:
        user = get_object_or_404(User, pk=user_id)
    else:
        user = User()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return redirect('shop:product_list')
    else:
        form = CustomUserCreationForm(instance=user)
        
    return render(request, 'accounts/edit.html', {'form':form})

class UserUpdateView(UpdateView):

    model = User
    fields = ('username', 'birthday',)
    template_name = 'accounts/edit.html'
    success_url = reverse_lazy('shop:product_list')

    def get_object(self):
        return self.request.user

class PasswordUpdateView(View):
    success_url = reverse_lazy('shop:product_list')
    def get(self, request, pk):
        form = PasswordUpdateForm()
        return render(request, 'accounts/password_edit.html', {'form':form})
  
    def post(self, request, pk):
        form = PasswordUpdateForm(request.POST)
        if form.is_valid():
            user = User.objects.get(pk=pk)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('accounts:profile', pk=user.id)
        
        else:
            return render(request, 'accounts/password_edit.html', {'form':form})

                 
class LoginView(AuthLoginView):

    #form_class = CustomUserCreationForm
    template_name = 'accounts/login.html'

class LogoutView(AuthLogoutView):
    template_name = 'accounts/logout.html'

    

    