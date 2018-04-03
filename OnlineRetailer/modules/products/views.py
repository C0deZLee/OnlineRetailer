from random import randrange

from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect

from .models import Product
from ..experiments.models import Settings, Record, Survey


def read_view(request):
	# if not request.session.get('session_set', False):
	request.session['cart'] = []
	request.session['exp_num'] = int(randrange(1, 5))
	request.session['repeat_count'] = 'Attempt 1'
	request.session['session_set'] = True
	ctx = {}
	if request.session.get('wrong_twice'):
		ctx['wrong_twice'] = True
	return render(request, 'read.html', ctx)


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
		# wrong twice
		if request.session.get('wrong'):
			request.session['wrong_twice'] = True
			return redirect('read')
		else:
			request.session['wrong'] = True
			ctx['wrong'] = True

	return render(request, 'read3.html', ctx)


def read4_view(request):
	if not request.session.get('session_set', False):
		return redirect('read')

	return render(request, 'read4.html')


def quiz_view(request):
	if not request.session.get('session_set', False):
		return redirect('read')
	ctx = {'exp_num': request.session['exp_num']}

	return render(request, 'quiz.html', ctx)


def product_list_view(request):
	if not request.session.get('session_set', False):
		return redirect('read')

	cart = request.session.get('cart', [])
	exp_num = request.session['exp_num']

	if request.session['repeat_count'] == 'Finished':
		return redirect('survey')

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

	product = request.session.get('cart', [])[0]
	exp_num = request.session['exp_num']
	total_score = 0.0
	raw_score = float(format(product['real_quality'] / product['price'], '.2f'))
	rank_score = 0
	for index, item in enumerate(Product.objects.filter(experiment_num=exp_num).order_by('-real_quality')):
		if str(item.title) == str(product['title']):
			rank = index + 1
			rank_score = float(format(rank / 20.0, '.2f'))
			total_score = float(format(raw_score + rank_score, '.2f'))
			new_record = Record(
				experiment_num=request.session['exp_num'],
				user_ip=user_ip,
				product_id=product['id'],
				product_fake_quality=product['fake_quality'],
				product_real_quality=product['real_quality'],
				raw_score=raw_score,
				rank=rank,
				total_score=total_score)
			new_record.save()

	page_title = request.session['repeat_count'] + ' Result'

	if request.session['repeat_count'] == 'Attempt 1':
		request.session['repeat_count'] = 'Attempt 2'
	elif request.session['repeat_count'] == 'Attempt 2':
		request.session['repeat_count'] = 'Attempt 3'
	elif request.session['repeat_count'] == 'Attempt 3':
		request.session['repeat_count'] = 'Finished'

	return render(request, 'confirmation.html',
	              {'title'       : page_title,
	               'product'     : product,
	               'total_score' : total_score,
	               'raw_score'   : raw_score,
	               'repeat_count': request.session['repeat_count']})


def survey_view(request):
	if request.method == 'GET':
		return render(request, 'survey.html')
	elif request.method == 'POST':
		if request.META.get('HTTP_X_FORWARDED_FOR'):
			user_ip = request.META.get('HTTP_X_FORWARDED_FOR')
		else:
			user_ip = request.META.get('REMOTE_ADDR')

		if request.POST['clarity'] == '0' or request.POST['satisfied'] == '0' or request.POST['gender'] == '0':
			return render(request, 'survey.html', {'error': 'Please fill the survey.'})
		Survey.objects.create(
			clarity=request.POST['clarity'],
			satisfied=request.POST['satisfied'],
			gender=request.POST['gender'],
			age=request.POST['age'],
			language=request.POST['language'],
			user_ip=user_ip
		)

		ctx = {}
		if request.session['repeat_count'] == 'Finished':
			setting = Settings.objects.first()
			ctx['code'] = setting.finish_code
			records = Record.objects.filter(user_ip=user_ip)
			highest_rank = 20
			for record in records:
				if record.rank < highest_rank:
					highest_rank = record.rank
			ctx['rank'] = highest_rank
			ctx['bonus'] = format(((21 - highest_rank) / 20.0) * 0.4, '.2f')
		return render(request, 'survey.html', ctx)


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
