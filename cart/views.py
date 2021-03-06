from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required

from store.models import Product

from .cart import Cart

@login_required
def cart_summary(request):
    cart = Cart(request)
    return render(request, 'cart/summary.html', {'cart': cart})

@login_required
def cart_add(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        product_qty = int(request.POST.get('productqty'))
        product = get_object_or_404(Product, id=product_id)
        cart.add(product=product, qty=product_qty)

        qty = cart.__len__()
        response = JsonResponse({'qty': qty})
        return response

@login_required
def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        cart.delete(product=product_id)

        qty = cart.__len__()
        total = cart.get_total_price()
        response = JsonResponse({'qty': qty, 'subtotal': total})
        return response

@login_required
def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        product_qty = int(request.POST.get('productqty'))
        cart.update(product=product_id, qty=product_qty)

        qty = cart.__len__()
        total = cart.get_total_price()
        response = JsonResponse({'qty': qty, 'subtotal': total})
        return response
