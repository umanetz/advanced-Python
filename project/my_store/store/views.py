from django.shortcuts import render
from django.http import HttpResponse
from .models import Category
import random
from datetime import datetime


random.seed(datetime.now())

# Create your views here.


def catalog(request):
    catalog_dict = {}
    main_categories = Category.objects.filter(is_active=True)
    for cat in main_categories:
        catalog_dict[cat.title] = Category.objects.filter(id=cat.id).all()[0]

    return render(request, 'store/catalog_main.html', {"dict": catalog_dict})