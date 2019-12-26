from django.contrib import admin
from .models import Cart, CartItem

# Register your models here.
class CartAdmin(admin.ModelAdmin):
    pass

class CartItemAdmin(admin.ModelAdmin):
    pass

admin.site.register(Cart)
admin.site.register(CartItem)
