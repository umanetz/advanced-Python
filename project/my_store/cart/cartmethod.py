from cart.models import Cart
import random, string
from django.contrib import messages
from django.core.cache import cache

TOKEN_LEN = 40


def __generate_token(_len):
    """ Генерирует случайный токен для корзины """
    return ''.join(random.choice(string.ascii_uppercase) for _ in range(_len))


def get_or_create_cart(request, response=None):
    
    """
    Возвращает последнюю корзину пользователя или создает новую.
    """
    cart = None
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.filter(customer=request.user.profile, released=False).latest('created_at')
            print('GET CART')
        except:    
            cart = Cart(customer=request.user.profile)
            cart.save()
            print('CREATE CART')
        
    return cart
    


def close_cart(_cart):
    """ Закрывает корзину. Вполне может стать сложнее. """
    _cart.released = True
    _cart.save()