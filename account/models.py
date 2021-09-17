import uuid
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)
from django.db import models

class CustomAccountManager(BaseUserManager):
    
    def create_superuser(self, email, user_name, password, **other_fields):
        
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be assigned to is_staff=True.')
        
        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must be assigned to is_superuser=True.')
        
        return self.create_user(email, user_name, password, **other_fields)
        
    def create_user(self, email, user_name, password, **other_fields):
        
        if not email:
            raise ValueError(_('You must provide an email address'))
        
        email = self.normalize_email(email)
        user = self.model(email=email, user_name=user_name, **other_fields)
        user.set_password(password)
        
        user.save()
        
        return user
    
class UserBase(AbstractBaseUser, PermissionsMixin):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    
    email = models.EmailField(unique=True)
    user_name = models.CharField(max_length=150, unique=True)
    full_name = models.CharField(max_length=255, blank=True)
    
    # User Status
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name']

    class Meta:
        verbose_name_plural = "users"
    
    def __str__(self):
        return self.user_name

class Shop(models.Model):
    user = models.OneToOneField(UserBase, related_name='shop', on_delete=models.CASCADE, primary_key=True)
    
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/')
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "shops"
    
    def __str__(self):
        return self.title
