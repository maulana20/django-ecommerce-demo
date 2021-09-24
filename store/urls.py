from django.urls import path

from . import views

app_name = 'store'

urlpatterns = [
    path('', views.all_products, name='all_products'),
    path('p/<slug:slug>', views.product_detail, name='product_detail'),
    path('c/<slug:category_slug>', views.category_list, name='category_list'),
    
    path('discussion', views.store_discussion, name='discussion'),
]
