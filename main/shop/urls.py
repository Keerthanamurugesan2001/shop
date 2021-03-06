from django.urls import path
from . import views

app_name = 'shop'
urlpatterns = [
    path('', views.view_item, name='view_item'),
    path('admin_view/add_stock/', views.add_stock, name='add_stock'),
    path('add_item_to_cart/', views.add_item_to_cart, name='add_item_to_cart'),
    path('<int:id>/', views.update_stock, name='update_stock'),
    path('admin_view/', views.admin_view, name='admin_view'),
]
