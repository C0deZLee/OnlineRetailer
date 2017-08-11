from django.db import models


class Product(models.Model):
	title = models.CharField(max_length=50)
	img = models.FileField(upload_to='product_imgs', null=True, blank=True)
	# description = models.TextField()
	fake_quality = models.IntegerField(default=0)
	real_quality = models.IntegerField(default=0)
	verified_quality = models.IntegerField(default=0)
	percentage = models.FloatField(default=0.0)
	coeff = models.FloatField(default=0.0)
	price = models.FloatField(default=0.0)
	amount = models.IntegerField(default=0)

	# related fields
	def __str__(self):
		return self.title

	def json(self):
		return {
			'id'              : self.id,
			'title'           : self.title,
			'price'           : self.price,
			'fake_quality'    : self.fake_quality,
			'real_quality'    : self.real_quality,
			'verified_quality': self.verified_quality
		}
