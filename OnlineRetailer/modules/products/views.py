from numpy import random

from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.utils import timezone

from .models import Product
from ..experiments.models import Settings, Record


def read_view(request):
	# if not request.session.get('session_set', False):
	request.session['cart'] = []
	request.session['exp_num'] = int(random.uniform(1, 3))
	request.session['repeat_count'] = 'Attempt 1'
	request.session['session_set'] = True
	return render(request, 'read.html')


def read1_view(request):
	if not request.session.get('session_set', False):
		return redirect('read')

	return render(request, 'read1.html')


def read2_view(request):
	if not request.session.get('session_set', False):
		return redirect('read')

	return render(request, 'read2.html')


def read3_view(request):
	if not request.session.get('session_set', False):
		return redirect('read')
	ctx = {'exp_num': request.session['exp_num']}
	if request.GET.get('wrong'):
		ctx['wrong'] = True
	return render(request, 'read3.html', ctx)


def read4_view(request):
	if not request.session.get('session_set', False):
		return redirect('read')

	return render(request, 'read4.html')


def quiz_view(request):
	if not request.session.get('session_set', False):
		return redirect('read')

	return render(request, 'quiz.html')


def quiz_check_view(request):
	if not request.session.get('session_set', False):
		return redirect('read')

	return render(request, 'quiz.html')


def product_list_view(request):
	if not request.session.get('session_set', False):
		return redirect('read')

	cart = request.session.get('cart', [])
	exp_num = request.session['exp_num']

	if request.session['repeat_count'] == 'Finished':
		return redirect('confirm')

	products_all = Product.objects.filter(experiment_num=exp_num)
	return render(request, 'list.html', {'products': products_all, 'cart': cart, 'title': 'Product List', 'repeat_count': request.session['repeat_count']})


def product_cart_view(request):
	if not request.session.get('session_set', False):
		return redirect('read')

	cart = request.session.get('cart', [])

	total = 0
	for product in cart:
		total += product['price']

	return render(request, 'cart.html', {'cart': cart, 'title': 'Shopping Cart', 'total': total})


def product_confirmation_view(request):
	if not request.session.get('session_set', False):
		return redirect('read')

	if request.META.get('HTTP_X_FORWARDED_FOR'):
		user_ip = request.META.get('HTTP_X_FORWARDED_FOR')
	else:
		user_ip = request.META.get('REMOTE_ADDR')

	cart = request.session.get('cart', [])
	exp_num = request.session['exp_num']
	setting = Settings.objects.first()

	rank_bonus = 0.0
	raw_score = 0.0
	total_score = 0.0

	for product in cart:
		raw_score = product['price'] / product['real_quality']
		raw_score = float(format(raw_score, '.2f'))
		for index, item in enumerate(Product.objects.filter(experiment_num=exp_num).order_by('real_quality')):
			if str(item.title) == str(product['title']):
				# rank_num = index
				rank_bonus = float(float(index) / 20.0)
				total_score = raw_score + rank_bonus
				total_score = format(total_score, '.2f')
				new_record = Record(
					experiment_num=request.session['exp_num'],
					user_ip=user_ip,
					product_id=product['id'],
					product_fake_quality=product['fake_quality'],
					product_real_quality=product['real_quality'],
					raw_score=raw_score,
					bonus=rank_bonus,
					total_score=total_score,
					created=timezone.now())
				new_record.save()

	page_title = request.session['repeat_count'] + ' Result'

	if request.session['repeat_count'] == 'Attempt 1':
		request.session['repeat_count'] = 'Attempt 2'
	elif request.session['repeat_count'] == 'Attempt 2':
		request.session['repeat_count'] = 'Attempt 3'
	elif request.session['repeat_count'] == 'Attempt 3':
		request.session['repeat_count'] = 'Finished'

	return render(request, 'confirmation.html',
	              {'code'        : setting.finish_code,
	               'title'       : page_title,
	               'cart'        : cart,
	               'total_score' : total_score,
	               'rank'        : rank_bonus,
	               'raw_score'   : raw_score,
	               'repeat_count': request.session['repeat_count']})


def add_to_cart(request, item_id):
	if not request.session.get('session_set', False):
		return redirect('read')

	product = Product.objects.get(id=item_id)
	request.session['cart'] = [product.json()]

	return redirect('cart')


def remove_from_cart(request, item_id):
	if not request.session.get('session_set', False):
		return redirect('read')

	cart = request.session.get('cart', [])

	product = Product.objects.get(id=item_id)
	cart.remove(product.json())

	return HttpResponseRedirect('/cart')
