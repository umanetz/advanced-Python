from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from pytils import translit
from django.dispatch import receiver
from django.db.models.signals import post_save




class Category(models.Model):
    title = models.CharField(max_length=100)
    img = models.ImageField(upload_to='img/catalog')
    translit_title = models.CharField(max_length=200, default='', blank=True)
    is_active = models.BooleanField()

    def save(self, *args, **kwargs):
        if not self.pk:  # object is being created, thus no primary key field yet
            self.translit_title = translit.slugify(self.title)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
        

class Product(models.Model):
    title = models.CharField(max_length=100)
    img = models.ImageField(upload_to='img/products')
    description = models.TextField()
    price = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category')
    translit_title = models.CharField(max_length=200, default='', blank=True)
    is_active = models.BooleanField()

    def save(self, *args, **kwargs):
        if not self.pk:  # object is being created, thus no primary key field yet
            self.translit_title = translit.slugify(self.title)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length = 20, default='', blank=True, null=True) 
    last_name = models.CharField(max_length = 20, default='', blank=True, null=True) 
    city = models.CharField("City", max_length=50, blank=True, null=True)


    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)




