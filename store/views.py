from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Cart




#главная страница
def product_list(request):
    products = Product.objects.all()
    return render(request, 'store/product_list.html', {'products': products})


#Корзина

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'store/cart.html',  {'cart_items': list(cart)})

def add_to_cart(request, product_id):
    cart = Cart(request)
    cart.add(product_id)
    print(request.session.get('cart'))
    return redirect('cart_detail')

def remove_from_cart(request, product_id):
    cart = Cart(request)
    cart.remove(product_id)
    return redirect('cart_detail')

