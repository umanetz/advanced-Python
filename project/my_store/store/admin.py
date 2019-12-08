from django.contrib import admin
from .models import Category

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active']
    ordering = ['title']
    list_filter = ['is_active']
    list_editable = ['is_active']
    
admin.site.register(Category, CategoryAdmin)