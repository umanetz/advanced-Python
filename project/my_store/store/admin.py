from django.contrib import admin
from .models import Category, Product

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active']
    ordering = ['title']
    list_filter = ['is_active']
    list_editable = ['is_active']
    

class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'category']
    ordering = ['title']
    list_filter = ['is_active']
    list_editable = ['is_active']
    

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)