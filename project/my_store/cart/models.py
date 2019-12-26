from django.db import models
from store.models import Profile, Product

from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


class Cart(models.Model):
    customer = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='carts')
    created_at = models.DateTimeField(default=datetime.now)
    released = models.BooleanField(default=False)
    total_price = models.IntegerField(default=0)
    max_count = 16

    def __str__(self):
        return self.customer.user.username + '-' + str(self.released)

    def save(self, *args, **kwargs):
        self.total_price = 0
        for el in self.cartitem_set.all():
            self.total_price += el.product.price * el.quantity
        super(Cart, self).save(*args, **kwargs)
    
    def item_count(self):
        count = 0
        for el in self.cartitem_set.all():
            count += el.quantity
        return count 


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)

    def __str__(self):
        return  self.user + " - " + self.product


# Create your models here.
