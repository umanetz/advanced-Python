from django import template
from cart.models import Cart
register = template.Library()

@register.filter(name='add_space')
def add_space(value):
    return '{0:,}'.format(value).replace(',', ' ')

@register.filter(name='cart_total_item')
def cart_total_item(user):
    count = 0 
    try:
        cart = Cart.objects.filter(customer=user.profile, released=False).latest('created_at')
    except:
        return count
    else:
        for el in cart.cartitem_set.all():
            count += el.quantity
        return count