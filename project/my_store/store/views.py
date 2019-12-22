from django.shortcuts import render, get_list_or_404, get_object_or_404, redirect, reverse
from django.http import HttpResponse
from .models import Category, Product, Profile
from django.contrib.auth import login, authenticate
from django.views import View
from django.views.generic import ListView, DetailView
from .forms import SignupForm, PasswordResetRequestForm, ProfileForm
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.views.generic.edit import FormView
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth.models import User


DEFAULT_FROM_EMAIL = 'umanetz.k@ya.ru'


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
            profile.email = form.cleaned_data['email']
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
                password=form.cleaned_data.get('password'))

            if user is None:
                return render(request, 'store/login.html', { 'form': form, 'invalid_creds': True })

            try:
                form.confirm_login_allowed(user)
            except ValidationError:
                return render(request, 'store/login.html', { 'form': form, 'invalid_creds': True })

            login(request, user)
            return redirect(reverse('profile'))
        return render(request, 'store/login.html', { 'form': form, 'categories': categories })


class ResetPasswordRequestView(FormView):
    template_name = 'store/reset_password.html'
    success_url = '/store/login'
    form_class = PasswordResetRequestForm

    def get(self, request):
        categories = Category.objects.filter(is_active=True)
        return render(request, self.template_name, { 'form':  self.form_class, 'categories': categories })

    @staticmethod
    def validate_email_address(email):
        try:
            validate_email(email)
            return True
        except ValidationError:
            return False

    def post(self, request, *args, **kwargs):
        categories = Category.objects.filter(is_active=True)
        form = self.form_class(request.POST)

        if form.is_valid():
            data= form.cleaned_data["email"]

        if self.validate_email_address(data) is True:  
            '''
            If the input is an valid email address, then the following code will lookup for users associated with that email address. If found then an email will be sent to the address, else an error message will be printed on the screen.
            '''
            user=User.objects.filter(email=data)
            if user.exists():
                user = user[0]
                new_password = 'dashasuper2'
                user.set_password(new_password)
                send_mail('Новый пароль', new_password, DEFAULT_FROM_EMAIL , [user.email], fail_silently=False)
                user.save()

                messages.success(request, 'Сообщение было отправлено на почту: ' + data)
                return redirect(reverse('user-login'))

            result = self.form_invalid(form)
            messages.error(request, 'Нет пользователя с таким адресом')
            return render(request, self.template_name, { 'form': form, 'categories': categories })

        messages.error(request, 'Неверно введен адрес')
        return render(request, self.template_name, { 'form': form,'categories': categories })


class ProfileView(FormView):
    default_img = Profile._meta.get_field('img').default

    def get(self, request):
        form = ProfileForm
        if request.user.is_authenticated and not request.user.is_superuser:
                profile = get_object_or_404(Profile, user__username=request.user.username)
                img = profile.img
                profile.username = profile.user.username
                return render(request, 'store/profile.html', {'profile': profile, 'form':form, 'delete_img':img!=self.default_img})
        return redirect(reverse('catalog'))
    
    def post(self, request):
        profile = request.user.profile
        form = ProfileForm(request.POST, request.FILES, instance=profile)

        if form.is_valid():
            if form.cleaned_data["delete"]:
                profile.set_image_to_default()

            if 'img' in request.FILES:
                form.photo = request.FILES['img']
            form.save()
        return redirect(reverse('profile'))
    

    
    
