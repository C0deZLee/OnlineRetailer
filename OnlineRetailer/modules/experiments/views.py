import csv
import numpy as np

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Survey, Record
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
		new_product.price = round(new_product.fake_quality ** 0.75)
	elif ability == 'H':
		if new_product.fake_quality >= new_product.verified_quality:
			new_product.price = round(new_product.verified_quality ** 0.75)
		else:
			new_product.price = round(new_product.fake_quality ** 0.75)
	return new_product


@login_required
def exp_control_view(request):
	line_count = Product.objects.all().count()
	return render(request, 'control.html', {'line': line_count})


@login_required
def random(request):
	# Experiment 1
	for i in range(1, 21):
		new_product = Product(
			title='Textbook ' + str(i),
			real_quality=round(np.random.uniform(30, 60, None)),
			amount=round(np.random.uniform(50, 70, None)),
			experiment_num=1
		)

		new_product = vendor_uncertainty_level(new_product, 'L')
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

		new_product = vendor_uncertainty_level(new_product, 'H')
		new_product = platform_detection_ability(new_product, 'H')
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

		new_product = vendor_uncertainty_level(new_product, 'L')
		new_product = platform_detection_ability(new_product, 'L')
		new_product = price_determination(new_product, 'L')

		new_product.save()

	# Experiment 4
	for i in range(1, 21):
		new_product = Product(
			title='Textbook ' + str(i),
			real_quality=round(np.random.uniform(30, 60, None)),
			amount=round(np.random.uniform(50, 70, None)),
			experiment_num=4
		)

		new_product = vendor_uncertainty_level(new_product, 'H')
		new_product = platform_detection_ability(new_product, 'L')
		new_product = price_determination(new_product, 'L')

		new_product.save()
	return redirect('control')


@login_required
def delete(request):
	Product.objects.all().delete()
	return redirect('control')


@login_required
def clean_session(request):
	request.session.flush()
	return redirect('control')


@login_required
def download_data(request):
	# Create the HttpResponse object with the appropriate CSV header.
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="data.csv"'

	writer = csv.writer(response)
	writer.writerow(['experiment_num', 'user_ip', 'product', 'product_fake_quality', 'product_real_quality', 'raw_score', 'rank', 'total_score', 'created'])

	for r in Record.objects.all():
		writer.writerow([r.experiment_num, r.user_ip, r.product, r.product_fake_quality, r.product_real_quality, r.raw_score, r.rank, r.total_score, r.created])

	return response


@login_required
def download_survey(request):
	# Create the HttpResponse object with the appropriate CSV header.
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="survey.csv"'

	writer = csv.writer(response)
	writer.writerow(['clarity', 'satisfied', 'gender', 'age', 'language', 'user_ip', 'created'])

	for s in Survey.objects.all():
		writer.writerow([s.clarity, s.satisfied, s.gender, s.age, s.language, s.user_ip, s.created])

	return response
