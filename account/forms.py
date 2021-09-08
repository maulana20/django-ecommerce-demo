from django import forms
from django.contrib.auth.forms import (AuthenticationForm)

from .models import UserBase

class UserLoginForm(AuthenticationForm):
    
    username = forms.EmailField(label='Email', min_length=5, max_length=50)
    password = forms.CharField(label='Password', min_length=5, max_length=50, widget=forms.PasswordInput())
    
    def __init__(self, *args, **kwargs):
        
        super().__init__(*args, **kwargs)
        
        self.fields['username'].widget.attrs.update({'class': 'form-control mb-3', 'placeholder': 'Email', 'id': 'login-username'})
        self.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password', 'id': 'login-pwd',})

class RegistrationForm(forms.ModelForm):
    
    user_name = forms.CharField(label='Enter Username', min_length=5, max_length=50, help_text='Required')
    email = forms.EmailField(label='Enter Email', min_length=5, max_length=50, help_text='Required', error_messages={'required': 'Sorry, you will need an email'})
    password = forms.CharField(label='Password', min_length=5, max_length=50, widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='Confirm Password', min_length=5, max_length=50, widget=forms.PasswordInput)
    
    class Meta:
        model = UserBase
        fields = ('user_name', 'email', 'password')
    
    def clean_username(self):
        user_name = self.cleaned_data['user_name'].lower()
        r = UserBase.objects.filter(user_name=user_name)
        
        if r.count():
            raise forms.ValidationError("Username already exists")
        
        return user_name
    
    def clean_confirmpassword(self):
        cd = self.cleaned_data
        
        if cd['password'] != cd['confirm_password']:
            raise forms.ValidationError('Confirm Password do not match.')
        
        return cd['confirm_password']
    
    def clean_email(self):
        email = self.cleaned_data['email']
        
        if UserBase.objects.filter(email=email).exists():
            raise forms.ValidationError('Please use another Email, that is already taken')
        
        return email
    
    def __init__(self, *args, **kwargs):
        
        super().__init__(*args, **kwargs)
        
        self.fields['user_name'].widget.attrs.update({'class': 'form-control mb-3', 'placeholder': 'Username'})
        self.fields['email'].widget.attrs.update({'class': 'form-control mb-3', 'placeholder': 'E-mail', 'name': 'email', 'id': 'id_email'})
        self.fields['password'].widget.attrs.update({'class': 'form-control mb-3', 'placeholder': 'Password'})
        self.fields['confirm_password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm Password'})

class UserEditForm(forms.ModelForm):
    
    email = forms.EmailField(label='Account email (can not be changed)', min_length=5, max_length=50)
    full_name = forms.CharField(label='Full name', min_length=5, max_length=100)
    
    class Meta:
        model = UserBase
        fields = ('email', 'full_name')
    
    def __init__(self, *args, **kwargs):
        
        super().__init__(*args, **kwargs)
        
        self.fields['email'].widget.attrs.update({'class': 'form-control mb-3', 'placeholder': 'email', 'id': 'form-email', 'readonly': 'readonly'})
        self.fields['full_name'].widget.attrs.update({'class': 'form-control mb-3', 'placeholder': 'Firstname', 'id': 'form-lastname'})
