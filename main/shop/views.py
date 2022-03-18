
from django.shortcuts import render, redirect
import sys

sys.path.append('/home/softsuave/PycharmProjects/shopapp/shopmain/shop/')
from .models import *
from .form import *
from django.contrib import messages
import shutil
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse


# # Create your views here.
def view_item(request):
    products = Product.objects.all()
    if request.method == 'POST':
        if request.user.is_authenticated and request.user.is_customer:
            product_id = int(request.POST.get('product_id'))
            product_check = Product.objects.get(id=product_id)
            product_qty = int(request.POST.get('quantity'))
            if product_check:
                if Cart.objects.filter(user=request.user.id, product=product_id):
                    t = Cart.objects.get(product=product_id)

                    if t.quantity < product_check.quantity:
                        t.quantity = product_qty
                        t.save()
                        messages.add_message(request, messages.SUCCESS, 'Product Added successfully')
                        return redirect('/')
                    else:
                        messages.add_message(request, messages.WARNING,
                                             'Only' + str(product_check.quantity) + 'is available')
                        return redirect('/')
                else:
                    print()
                    Cart.objects.create(product=product_check, user=request.user, quantity=product_qty)
                    messages.add_message(request, messages.SUCCESS, 'Product Added successfully')
                    return redirect('/')
            else:
                messages.add_message(request, messages.WARNING, 'No such product found')
                return redirect('/')
        else:
            messages.add_message(request, messages.WARNING, "your'e admin please Login to continue")
            return redirect('/login/')
        return render(request, 'shop/add_item_to_cart.html', {})

    return render(request, "shop/view_item.html", {'products': products})


def admin_view(request):
    products = Product.objects.all
    if request.method == "POST":
        # see user is admin
        if request.user.is_authenticated and request.user.is_admin:
            if request.POST.get("delete"):
                print(request.POST.get('getedvalue'))
                item = request.POST.get('getedvalue')
                t = Product.objects.get(id=item)
                t.delete()
                messages.add_message(request, messages.WARNING, "Product deleted successfully")
            elif request.POST.get("edit"):
                i = int(request.POST.get('getedvalue'))
                return HttpResponseRedirect('/%d' % i)
        else:
            messages.add_message(request, messages.WARNING, "Your'e not admin")

    return render(request, "shop/admin_view.html", {'products': products})


def add_stock(request):
    if request.method == "POST":
        form = Addstock(request.POST, request.FILES)
        # see user is admin
        if request.user.is_authenticated and request.user.is_admin:
            if form.is_valid():
                user = request.user
                productname = form.cleaned_data.get('productname')
                price = form.cleaned_data.get('price')
                description = form.cleaned_data.get('description')
                productimage = form.cleaned_data.get('productimage')
                quantity = form.cleaned_data.get('quantity')
                s = Product.objects.create(user=user, productname=productname, price=price, description=description,
                                           productimage=productimage, quantity=quantity)

                s.save()
                messages.add_message(request, messages.SUCCESS, "Product added successfully")
                return redirect('/admin_view')
        else:
            messages.add_message(request, messages.WARNING, "Your'e not admin")
    else:
        form = Addstock()
    return render(request, "shop/add_stock.html", {'form': form})


def add_item_to_cart(request):
    form = Cart.objects.all
    if request.method == 'POST':
        if request.user.is_authenticated and request.user.is_customer:
            if request.POST.get('remove'):
                id = request.POST.get('removefield')
                t = Cart.objects.get(id=id)
                t.delete()
        else:
            messages.add_message(request, messages.WARNING, "Your'e admin you can't change this stuff")
    else:
        form = Cart.objects.all
    return render(request, 'shop/add_item_to_cart.html', {'form': form})


def update_stock(request, id):
    item = Product.objects.get(id=id)
    print(item)
    product_data = {
        'productname': item.productname,
        'price': item.price,
        'description': item.description,
        'productimage': item.productimage,
        'quantity': item.quantity,
    }
    form = Addstock(initial=product_data)

    if request.method == "POST":
        if request.user.is_authenticated and request.user.is_admin:
            form = Addstock(request.POST, request.FILES)

            if form.is_valid():
                productname = form.cleaned_data.get('productname')
                price = form.cleaned_data.get('price')
                description = form.cleaned_data.get('description')
                productimage = form.cleaned_data.get('productimage')
                quantity = form.cleaned_data.get('quantity')
                if productimage is None:
                    productimage = item.productimage
                if productname != item.productname:
                    item.productname = productname
                    item.save()
                if price != item.price:
                    item.price = price
                    item.save()
                if description != item.description:
                    item.description = description
                    item.save()
                if productimage != item.productimage:
                    item.productimage = productimage
                    item.save()
                if quantity != item.quantity:
                    item.quantity = quantity
                    item.save()
                messages.add_message(request, messages.SUCCESS, "item updated")
                return redirect('/admin_view')
        else:
            messages.add_message(request, messages.WARNING, "Your'e not admin")
    else:
        form = Addstock(initial=product_data)
    return render(request, 'shop/add_stock.html/', {'form': form})

