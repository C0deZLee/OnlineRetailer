import numpy as np
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from ..products.models import Product


@login_required
def exp_control_view(request):
	line_count = Product.objects.all().count()
	return render(request, 'control.html', {'line': line_count})


@login_required
def random(request):
	# How to create new Product:
	# one way: new_product = Product(price=10, title='Shoes', ....)
	# second way: new_product = Product()    new_product.title='Shoes'

	# How to save your new product to databse:
	# new_product.save()

	for i in range(1, 101):
		new_product = Product()
		new_product.title = 'Textbook ' + str(i)
		new_product.real_quality = round(np.random.uniform(30, 60, None))
		new_product.amount = round(np.random.uniform(50, 70, None))

		def vendor_uncertainty_level(level):
			if level == 'H':
				new_product.coeff = np.random.uniform(1, 1.5)
				new_product.fake_quality = new_product.coeff * new_product.real_quality
				return round(new_product.fake_quality)
			elif level == 'L':
				new_product.coeff = np.random.uniform(1, 1.2)
				new_product.fake_quality = new_product.coeff * new_product.real_quality
				return round(new_product.fake_quality)
			else:
				return 'Wrong information'

		# print (real_quality, vendor_uncertainty_level('L'))
		new_product.fake_quality = vendor_uncertainty_level('L')

		def platform_detection_ability(ability):
			if ability == 'L':
				new_product.verified_quality = new_product.fake_quality
				return round(new_product.verified_quality)
			elif ability == 'H':
				new_product.percentage = np.random.uniform(0.01, 0.1, None)
				new_product.verified_quality = new_product.real_quality + new_product.real_quality * new_product.percentage
				return round(new_product.verified_quality)
			else:
				return 'Wrong information'

		# print (platform_detection_ability('H'))
		new_product.verified_quality = platform_detection_ability('H')

		def price_determination(ability):
			if ability == 'L':
				new_product.price = new_product.fake_quality / 3.0
				return round(new_product.price)
			elif ability == 'H':
				if new_product.fake_quality >= new_product.verified_quality:
					new_product.price = new_product.verified_quality / 3.0
				else:
					new_product.price = new_product.fake_quality / 3.0
				return round(new_product.price, 2)

		new_product.price = price_determination('H')
		# print (price_determination('H'))
		# print(real_quality, claimed_quality, verified_quality, price)
		i += 1
		new_product.save()
	return redirect('control')


@login_required
def delete(request):
	Product.objects.all().delete()
	return redirect('control')
