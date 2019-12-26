from django.shortcuts import render
from django.shortcuts import render, get_list_or_404, get_object_or_404, redirect, reverse
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from .models import Cart, CartItem
from store.models import Product
from .cartmethod import get_or_create_cart, close_cart
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect




##-------------- Cart Views --------------------------------------

def cart_detail(request):
    cart = get_or_create_cart(request)
    # if not cart:
    #     messages.error(request, f'Пожалуйста, авторизуйтесь')
    return render(request, 'cart/cart.html', {'cart':cart})


def cart_add(request, pk_item):
    cart = get_or_create_cart(request)
    product = get_object_or_404(Product, pk = pk_item)
    category_name = product.category.translit_title

    if not cart:
        messages.error(request, 'Пожалуйста, авторизуйтесь')
        return redirect('item-detail', category_name = category_name, pk=pk_item)
        
    count = cart.item_count()
    if count >= Cart.max_count:
        messages.error(request, f'Максимальное количество товаров в корзине {Cart.max_count}')
        return redirect('item-detail', category_name = category_name, pk=pk_item)
    
    cart_item = CartItem.objects.filter(product=product, cart=cart)

    if not cart_item:
        CartItem(product=product, cart=cart).save()
    else:
        cart_item[0].quantity += 1
        cart_item[0].save()
    cart.save()
    return redirect('item-detail', category_name = category_name, pk=pk_item)
    
    
