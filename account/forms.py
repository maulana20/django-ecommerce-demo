from django import forms
from django.contrib.auth.forms import (AuthenticationForm)

from .models import User

class UserLoginForm(AuthenticationForm):
    user_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Username', 'id': 'login-username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password', 'id': 'login-pwd',}))

class RegistrationForm(forms.ModelForm):
    user_name = forms.CharField(label='Enter Username', min_length=4, max_length=50, help_text='Required')
    email = forms.EmailField(max_length=100, help_text='Required', error_messages={'required': 'Sorry, you will need an email'})
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ('user_name', 'email', 'password')
    
    def clean_username(self):
        user_name = self.cleaned_data['user_name'].lower()
        r = User.objects.filter(user_name=user_name)
        
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
        
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Please use another Email, that is already taken')
        
        return email
    
    def __init__(self, *args, **kwargs):
        
        super().__init__(*args, **kwargs)
        
        self.fields['user_name'].widget.attrs.update({'class': 'form-control mb-3', 'placeholder': 'Username'})
        self.fields['email'].widget.attrs.update({'class': 'form-control mb-3', 'placeholder': 'E-mail', 'name': 'email', 'id': 'id_email'})
        self.fields['password'].widget.attrs.update({'class': 'form-control mb-3', 'placeholder': 'Password'})
        self.fields['confirm_password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm Password'})
