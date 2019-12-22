from django.shortcuts import render, get_list_or_404, get_object_or_404, redirect, reverse
from django.http import HttpResponse
from .models import Category, Product, Profile
from django.contrib.auth import login, authenticate
from django.views import View
from django.views.generic import ListView, DetailView
from .forms import SignupForm
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm



class CategoryList(ListView):
    template_name = 'store/catalog_category.html'
    context_object_name = 'products'


    def get_context_data(self, **kwargs):
        context = super(CategoryList, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(is_active=True)
        return context

    def get_queryset(self):
        name = self.kwargs['category_name']
        if name in [obj.translit_title for obj in Category.objects.filter(is_active=True)]:
            objects = Product.objects.filter(category__translit_title=name, is_active=True)
        else:
            objects = get_list_or_404(Product, category__translit_title=self.kwargs['category_name'], is_active=True)
        return objects


class ItemDetail(DetailView):
    template_name = 'store/item.html'
    context_object_name = 'item'
    queryset = Product.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
            context = super(ItemDetail, self).get_context_data(**kwargs)
            context['categories'] = Category.objects.filter(is_active=True)
            return context


class Catalog(ListView):
    queryset = Category.objects.filter(is_active=True)
    context_object_name = 'categories'
    template_name = 'store/catalog_main.html'

class RegisterView(View):
    def get(self, request):
        categories = Category.objects.filter(is_active=True)
        if request.user.is_authenticated:
            return redirect(reverse('catalog'))
        return render(request, 'store/register.html', { 'form': SignupForm() ,'categories': categories})

    def post(self, request):
        form = SignupForm(request.POST)
        categories = Category.objects.filter(is_active=True)
        if form.is_valid():
            user = form.save()

            profile = Profile()
            profile.user = user
            profile.save()

            return redirect(reverse('user-login'))

        return render(request, 'store/register.html', { 'form': form,'categories': categories })


class LoginView(View):
    def get(self, request):
        categories = Category.objects.filter(is_active=True)
        return render(request, 'store/login.html', { 'form':  AuthenticationForm,'categories': categories })

    # really low level
    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        categories = Category.objects.filter(is_active=True)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password')
            )

            if user is None:
                return render(
                    request,
                    'store/login.html',
                    { 'form': form, 'invalid_creds': True }
                )

            try:
                form.confirm_login_allowed(user)
            except ValidationError:
                return render(
                    request,
                    'store/login.html',
                    { 'form': form, 'invalid_creds': True }
                )
            login(request, user)
            return redirect(reverse('catalog'))
        print(form.errors)
        return render(request, 'store/login.html', { 'form': form,'categories': categories })
