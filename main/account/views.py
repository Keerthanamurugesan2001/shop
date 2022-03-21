# views.py
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import *
from django.contrib.auth import authenticate, login, get_user_model
from django.conf import settings
from django.contrib import messages

User = settings.AUTH_USER_MODEL


# Create your views here.
def register(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = response.user
            obj.save()
            if response.user.is_customer:
                return HttpResponseRedirect(reverse('shop:view_item'))
            else:
                # return redirect('/admin_view/')
                return HttpResponseRedirect(reverse('shop:admin_view'))
        else:
            messages.add_message(response, messages.SUCCESS, "Your'e BUY SUCCESSFULLY")
    else:
        form = RegisterForm()

    return render(response, "register/register.html", {"form": form})


def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None and user.is_admin:
                login(request, user)
                return HttpResponseRedirect(reverse('shop:admin_view'))
            elif user is not None and user.is_customer:
                login(request, user)
                return HttpResponseRedirect(reverse('shop:view_item'))
            else:
                messages.add_message(request, messages.SUCCESS, "username or password is incorrecr")
        else:
            msg = 'error in validating form'

    return render(request, 'registration/login.html', {"form": form, 'msg': msg})


