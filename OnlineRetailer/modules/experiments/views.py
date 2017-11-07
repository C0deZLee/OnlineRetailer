import numpy as np
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from ..products.models import Product


# Utility
def vendor_uncertainty_level(new_product, level):
	if level == 'H':
		new_product.coeff = np.random.uniform(1, 1.5)
		new_product.fake_quality = round(new_product.coeff * new_product.real_quality)
	elif level == 'L':
		new_product.coeff = np.random.uniform(1, 1.2)
		new_product.fake_quality = round(new_product.coeff * new_product.real_quality)
	return new_product


def platform_detection_ability(new_product, ability):
	if ability == 'L':
		new_product.verified_quality = round(new_product.fake_quality)
	elif ability == 'H':
		new_product.percentage = np.random.uniform(0.01, 0.1, None)
		new_product.verified_quality = round(new_product.real_quality + new_product.real_quality * new_product.percentage)
	return new_product


def price_determination(new_product, ability):
	if ability == 'L':
		new_product.price = round(new_product.fake_quality / 3.0)
	elif ability == 'H':
		if new_product.fake_quality >= new_product.verified_quality:
			new_product.price = round(new_product.verified_quality / 3.0)
		else:
			new_product.price = round(new_product.fake_quality / 3.0)
	return new_product


@login_required
def exp_control_view(request):
	line_count = Product.objects.all().count()
	return render(request, 'control.html', {'line': line_count})


@login_required
def random(request):
	# Experiment 0
	for i in range(1, 21):
		new_product = Product(
			title='Textbook ' + str(i),
			real_quality=round(np.random.uniform(30, 60, None)),
			amount=round(np.random.uniform(50, 70, None)),
			experiment_num=0
		)

		new_product = vendor_uncertainty_level(new_product, 'L')
		new_product = platform_detection_ability(new_product, 'H')
		new_product = price_determination(new_product, 'H')

		new_product.save()

	# Experiment 1
	for i in range(1, 21):
		new_product = Product(
			title='Textbook ' + str(i),
			real_quality=round(np.random.uniform(30, 60, None)),
			amount=round(np.random.uniform(50, 70, None)),
			experiment_num=1
		)

		new_product = vendor_uncertainty_level(new_product, 'H')
		new_product = platform_detection_ability(new_product, 'H')
		new_product = price_determination(new_product, 'H')

		new_product.save()

	# Experiment 2
	for i in range(1, 21):
		new_product = Product(
			title='Textbook ' + str(i),
			real_quality=round(np.random.uniform(30, 60, None)),
			amount=round(np.random.uniform(50, 70, None)),
			experiment_num=2
		)

		new_product = vendor_uncertainty_level(new_product, 'L')
		new_product = platform_detection_ability(new_product, 'L')
		new_product = price_determination(new_product, 'H')

		new_product.save()

	# Experiment 3
	for i in range(1, 21):
		new_product = Product(
			title='Textbook ' + str(i),
			real_quality=round(np.random.uniform(30, 60, None)),
			amount=round(np.random.uniform(50, 70, None)),
			experiment_num=3
		)

		new_product = vendor_uncertainty_level(new_product, 'H')
		new_product = platform_detection_ability(new_product, 'L')
		new_product = price_determination(new_product, 'H')

		new_product.save()
	return redirect('control')


@login_required
def delete(request):
	Product.objects.all().delete()
	return redirect('control')


def clean_session(request):
	request.session['session_set'] = False
	return redirect('control')
