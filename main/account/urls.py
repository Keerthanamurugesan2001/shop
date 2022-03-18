from django.urls import path, include
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    # path('', include("django.contrib.auth.urls")),
    path('login/', views.login_view, name='login'),
    path('home/', views.home, name='home')
]

