from django.shortcuts import get_object_or_404, render

from .forms import CommentForm, ReplyForm
from .models import Category, Product, Comment

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

def store_discussion(request):
    
    if hasattr(request.user, 'shop') == True:
        comments = Comment.objects.filter(product__in=request.user.shop.products.values_list('pk', flat=True))
    else:
        comments = Comment.objects.filter(user=request.user)
    
    if request.method == 'POST':
        
        replyForm = ReplyForm(data=request.POST)
        
        if replyForm.is_valid():
            reply = replyForm.save(commit=False)
            reply.user = request.user
            
            reply.save()
            
            replyForm = ReplyForm()
    else:
        replyForm = ReplyForm()
    
    return render(request, 'store/discussion/home.html', {'comments': comments, 'form': replyForm})

def page_not_found_view(request, exception):
    return render(request, 'core/404.html', status=404)
