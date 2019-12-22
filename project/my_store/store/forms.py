from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=20)

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')
