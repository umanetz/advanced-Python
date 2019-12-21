from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class SignupForm(UserCreationForm):
    # city = forms.CharField(required=False)
    # first_name = forms.CharField(max_length = 20, required=False) 
    # last_name = forms.CharField(max_length = 20, required=False) 

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')
