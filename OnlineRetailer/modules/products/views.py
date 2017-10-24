from numpy import random

from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.utils import timezone

from .models import Product
from ..experiments.models import Settings, Record


def product_list_view(request):
	if not request.session.get('session_set', False):
		cart = request.session['cart'] = []
		exp_num = request.session['exp_num'] = int(random.uniform(1, 3))
		request.session['repeat_count'] = 0
		request.session['session_set'] = True
	else:
		cart = request.session.get('cart', [])
		exp_num = request.session['exp_num']
		if request.session['repeat_count'] == 0:
			request.session['repeat_count'] = 1
		elif request.session['repeat_count'] == 1:
			request.session['repeat_count'] = 2
		elif request.session['repeat_count'] == 2:
			request.session['repeat_count'] = 3
		else:
			setting = Settings.objects.first()
			return render(request, 'confirmation.html',
			              {'code'        : setting.finish_code,
			               'title'       : 'Confirmation',
			               'repeat_count': request.session['repeat_count']})

	products_all = Product.objects.filter(experiment_num=exp_num)

	return render(request, 'list.html', {'products': products_all, 'cart': cart, 'title': 'Product List', 'repeat_count': request.session['repeat_count']})


def product_cart_view(request):
	if not request.session.get('session_set', False):
		cart = request.session['cart'] = []
		exp_num = request.session['exp_num'] = int(random.uniform(1, 3))
		request.session['session_set'] = True
	else:
		cart = request.session.get('cart', [])
		exp_num = request.session['exp_num']

	total = 0
	for product in cart:
		total += product['price']

	return render(request, 'cart.html', {'cart': cart, 'title': 'Shopping Cart', 'total': total})


def product_confirmation_view(request):
	if not request.session.get('session_set', False):
		cart = request.session['cart'] = []
		exp_num = request.session['exp_num'] = int(random.uniform(1, 3))
		request.session['session_set'] = True
	else:
		cart = request.session.get('cart', [])
		exp_num = request.session['exp_num']

	setting = Settings.objects.first()

	score = 0
	rank_bonus = 0.0

	for product in cart:
		score += product['price'] / product['real_quality']

		for index, item in enumerate(Product.objects.filter(experiment_num=exp_num).order_by('real_quality')):
			if str(item.title) == str(product['title']):
				rank_bonus = float(float(index) / 50.0)
				score += rank_bonus
				new_record = Record(score=score, product_id=product['id'], created=timezone.now())
				new_record.save()

	return render(request, 'confirmation.html',
	              {'code'        : setting.finish_code,
	               'title'       : 'Confirmation',
	               'cart'        : cart,
	               'score'       : score,
	               'rank'        : rank_bonus,
	               'repeat_count': request.session['repeat_count']})


def add_to_cart(request, item_id):
	if not request.session.get('session_set', False):
		cart = request.session['cart'] = []
		exp_num = request.session['exp_num'] = int(random.uniform(1, 3))
		request.session['session_set'] = True
	else:
		cart = request.session.get('cart', [])
		exp_num = request.session['exp_num']

	product = Product.objects.get(id=item_id)

	request.session['cart'] = [product.json()]

	return redirect('cart')


def remove_from_cart(request, item_id):
	if not request.session.get('session_set', False):
		cart = request.session['cart'] = []
		exp_num = request.session['exp_num'] = int(random.uniform(1, 3))
		request.session['session_set'] = True
	else:
		cart = request.session.get('cart', [])
		exp_num = request.session['exp_num']

	product = Product.objects.get(id=item_id)
	cart.remove(product.json())

	return HttpResponseRedirect('/cart')
