from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.conf import settings

from account.models import Shop

class ProductManager(models.Manager):
    def get_queryset(self):
        return super(ProductManager, self).get_queryset().filter(is_active=True, in_stock=True)

class Category(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True)

    class Meta:
        verbose_name_plural = 'categories'

    def get_absolute_url(self):
        return reverse('store:category_list', args=[self.slug])

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='product', on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='products', blank=True, null=True)
    
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='images/')
    slug = models.SlugField(max_length=255, unique=True)
    price = models.FloatField()
    
    in_stock = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    objects = models.Manager()
    products = ProductManager()
    
    class Meta:
        verbose_name_plural = 'products'
        ordering = ('-created',)

    def get_absolute_url(self):
        return reverse('store:product_detail', args=[self.slug])

    def __str__(self):
        return self.title

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    
    body = models.TextField(max_length=500, blank=True)
    
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'comments'
        ordering = ('-created',)
    
    def __str__(self):
        return 'Comment {}' . format(self.body)

class Reply(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replies')
    
    body = models.TextField(max_length=500, blank=True)
    
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'replies'
        ordering = ('created',)
    
    def __str__(self):
        return 'Reply {}' . format(self.body)
