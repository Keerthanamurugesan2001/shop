from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class RegisterForm(UserCreationForm):

    email = forms.EmailField(max_length=200)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2", "is_admin", "is_customer"]


class LoginForm(forms.Form):
    username = forms.CharField(max_length=200)
    password = forms.CharField(max_length=200)