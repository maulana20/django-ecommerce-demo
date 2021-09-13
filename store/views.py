from django.shortcuts import get_object_or_404, render

from .forms import CommentForm
from .models import Category, Product

def all_products(request):
    products = Product.products.all()
    return render(request, 'store/home.html', {'products': products})

def category_list(request, category_slug=None):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.products.filter(category=category)
    return render(request, 'store/products/category.html', {'category': category, 'products': products})

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, in_stock=True)
    
    if request.method == 'POST':
        
        commentForm = CommentForm(data=request.POST)
        
        if commentForm.is_valid():
            comment = commentForm.save(commit=False)
            comment.product = product
            comment.user = None if request.user.is_anonymous == True else request.user
            
            comment.save()
            
            commentForm = CommentForm()
    else:
        commentForm = CommentForm()
    
    return render(request, 'store/products/detail.html', {'product': product, 'form': commentForm})

def page_not_found_view(request, exception):
    return render(request, 'core/404.html', status=404)
