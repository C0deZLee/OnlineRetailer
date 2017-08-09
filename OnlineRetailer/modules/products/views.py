from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse

from .models import Product
from ..experiments.models import Settings


def product_list_view(request, page=None):
    cart = request.session.get('cart', [])
    request.session['cart'] = cart

    products_all = Product.objects.all()
    paginator = Paginator(products_all, 100)

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        products = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        products = paginator.page(paginator.num_pages)

    return render(request, 'list.html', {'products': products, 'cart': cart, 'title': 'Product List'})


def product_cart_view(request):
    cart = request.session.get('cart', [])
    request.session['cart'] = cart

    setting = Settings.objects.first()

    total = 0
    for product in cart:
        total += product['price']

    return render(request, 'cart.html', {'cart': cart, 'title': 'Shopping Cart',
                                         #'money': setting.max_money,
                                         'total': total})


def product_confirmation_view(request):
    cart = request.session.get('cart', [])
    request.session['cart'] = []
    setting = Settings.objects.first()

    score = 0

    for item in cart:
        score += item['price'] / item['real_quality']
    return render(request, 'confirmation.html', {'code': setting.finish_code, 'title': 'Confirmation', 'cart': cart, 'score': score})


def add_to_cart(request, item_id):
    cart = request.session.get('cart', [])
    request.session['cart'] = cart

    product = Product.objects.get(id=item_id)
    cart.append(product.json())
    return HttpResponseRedirect('/')


def remove_from_cart(request, item_id):
    cart = request.session.get('cart', [])
    request.session['cart'] = cart

    product = Product.objects.get(id=item_id)
    cart.remove(product.json())
    return HttpResponseRedirect('/cart')
