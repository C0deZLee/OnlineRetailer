from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.utils import timezone

from .models import Product
from ..experiments.models import Settings, Record


def product_list_view(request, page=None):
	cart = request.session.get('cart', [])
	request.session['cart'] = cart

	products_all = Product.objects.all()
	# paginator = Paginator(products_all, 100)

	# try:
	# 	products = paginator.page(page)
	# except PageNotAnInteger:
	# 	# If page is not an integer, deliver first page.
	# 	products = paginator.page(1)
	# except EmptyPage:
	# 	# If page is out of range (e.g. 9999), deliver last page of results.
	# 	products = paginator.page(paginator.num_pages)

	return render(request, 'list.html', {'products': products_all, 'cart': cart, 'title': 'Product List'})


def product_cart_view(request):
	cart = request.session.get('cart', [])
	request.session['cart'] = cart

	# setting = Settings.objects.first()

	total = 0
	for product in cart:
		total += product['price']

	return render(request, 'cart.html', {'cart' : cart, 'title': 'Shopping Cart',
	                                     # 'money': setting.max_money,
	                                     'total': total})


def product_confirmation_view(request):
	cart = request.session.get('cart', [])
	request.session['cart'] = []
	setting = Settings.objects.first()

	score = 0
	rank_bonus = 0.0

	for product in cart:
		score += product['price'] / product['real_quality']

		for index, item in enumerate(Product.objects.order_by('real_quality')):
			if str(item.title) == str(product['title']):
				rank_bonus = float(index / 100)
				score += rank_bonus
				new_record = Record(score=score, product_id=product['id'], created=timezone.now())
				new_record.save()

	return render(request, 'confirmation.html', {'code': setting.finish_code, 'title': 'Confirmation', 'cart': cart, 'score': score, 'rank': rank_bonus})


def add_to_cart(request, item_id):
	cart = request.session.get('cart', [])
	request.session['cart'] = cart
	product = Product.objects.get(id=item_id)

	request.session['cart'] = [product.json()]

	return redirect('cart')


def remove_from_cart(request, item_id):
	cart = request.session.get('cart', [])
	request.session['cart'] = cart

	product = Product.objects.get(id=item_id)
	cart.remove(product.json())

	return HttpResponseRedirect('/cart')
