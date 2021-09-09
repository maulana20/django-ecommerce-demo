from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login, logout
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse

from django.template.loader import render_to_string

from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from django.core.mail import send_mail

from .forms import (RegistrationForm, UserEditForm, UserLoginForm)
from .tokens import account_activation_token

from .models import UserBase

@login_required
def dashboard(request):
    return render(request, 'account/dashboard.html', {'section': 'profile'})

@login_required
def account_edit(request):
    
    if request.method == 'POST':
        editForm = UserEditForm(instance=request.user, data=request.POST)
        
        if editForm.is_valid():
            user = UserBase.objects.get(id=request.user.id)
            user.full_name = request.POST['full_name']
            
            user.save()
    else:
        editForm = UserEditForm(instance=request.user)
    
    return render(request, 'account/edit.html', {'form': editForm})

def account_login(request):
    
    if request.method == 'POST':
        loginForm = UserLoginForm(request.POST)
        
        if loginForm.is_valid():
            user = authenticate(request, email=request.POST["email"], password=request.POST["password"])
            
            if user:
                if user.is_superuser == True:
                    loginForm.add_error(None, 'Not for admin!')
                else:
                    login(request, user)
                    return redirect('account:dashboard')
            else:
                loginForm.add_error(None, 'Error: Username or Password not correct!')
    else:
        loginForm = UserLoginForm()
    
    return render(request, 'account/auth/login.html', {'form': loginForm})

def account_register(request):
    
    if request.user.is_authenticated:
        return redirect('account:dashboard')
    
    if request.method == 'POST':
        
        registerForm = RegistrationForm(request.POST)
        
        if registerForm.is_valid():
            
            user = registerForm.save(commit=False)
            user.email = registerForm.cleaned_data['email']
            user.set_password(registerForm.cleaned_data['password'])
            user.is_active = False
            
            user.save()
            
            send_mail(
                'Activate your Account',
                render_to_string('email/auth/confirm_email.html', {
                    'user': user,
                    'domain': get_current_site(request).domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                }),
                'djangoecommerce@example.com',
                [user.email],
                fail_silently=False,
            )
            
            return HttpResponse('registered succesfully and activation sent')
    else:
        registerForm = RegistrationForm()
    
    return render(request, 'account/auth/register.html', {'form': registerForm})

def account_verify(request, uidb64, token):
    
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = UserBase.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, user.DoesNotExist):
        user = None
    
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        
        login(request, user)
        
        return redirect('account:dashboard')
    
    return render(request, 'account/auth/verify_invalid.html')
