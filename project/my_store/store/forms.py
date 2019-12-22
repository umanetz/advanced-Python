from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Profile


class SignupForm(UserCreationForm):
    username = forms.CharField(max_length=20,  label='Username')
    password1 = forms.CharField(max_length=20, min_length=8, widget=forms.PasswordInput, label='Пароль', 
                                help_text = 'Your password must contain at least 8 characters')
    password2 = forms.CharField(label='Подтвердите пароль', widget=forms.PasswordInput)

    email = forms.EmailField(max_length=50)
    
    def clean_email(self):
        # Get the email
        email = self.cleaned_data.get('email')

        # Check to see if any users already exist with this email as a username.
        try:
            match = User.objects.get(email=email)
        except User.DoesNotExist:
            # Unable to find a user, this is fine
            return email

        # A user was found with this as a username, raise an error.
        raise forms.ValidationError('This email address is already in use.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class PasswordResetRequestForm(forms.Form):
    email = forms.CharField(label=("Email"), max_length=254)


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=20,  label='Имя', required=False)
    last_name = forms.CharField(max_length=20,  label='Фамилия', required=False)
    city = forms.CharField(max_length=20,  label='Город', required=False)
    img = forms.ImageField(label='загрузить фото', required=False)
    delete = forms.BooleanField(required=False)

    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'city', 'img', 'delete')

