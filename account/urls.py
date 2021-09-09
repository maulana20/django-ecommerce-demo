from django.contrib.auth import views as auth_views
from django.urls import path

from . import views
from .forms import (UserLoginForm)

app_name = 'account'

urlpatterns = [
    path('login', views.account_login, name='login'),
    path('logout', auth_views.LogoutView.as_view(next_page='/account/login'), name='logout'),
    
    path('register', views.account_register, name='register'),
    path('verify-email/<slug:uidb64>/<slug:token>)', views.account_verify, name='verify-email'),
    
    path('dashboard', views.dashboard, name='dashboard'),
    
    path('edit', views.account_edit, name='edit'),
]
