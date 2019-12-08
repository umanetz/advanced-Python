from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from pytils import translit


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
        

# class Product(models.Model):
#     title = models.CharField(max_length=100)
#     img = models.ImageField(upload_to='img/products')
#     description = models.TextField()
#     price = models.IntegerField()

#     category = models.ForeignKey(Category, null=True)

#     translit_title = models.CharField(max_length=200, default='')

#     def save(self, *args, **kwargs):
#         if not self.pk:  # object is being created, thus no primary key field yet
#             self.translit_title = translit.slugify(self.title)
#         super(Product, self).save(*args, **kwargs)

#     def __str__(self):
#         return self.title


