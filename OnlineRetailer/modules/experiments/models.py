from django.db import models


class Record(models.Model):
	experiment_num = models.IntegerField(default=0)
	user_ip = models.CharField(max_length=20, null=True, blank=True)
	product = models.ForeignKey('products.Product', on_delete=models.PROTECT)
	product_fake_quality = models.FloatField(default=0.0)
	product_real_quality = models.FloatField(default=0.0)

	raw_score = models.FloatField(default=0.0)
	bonus = models.FloatField(default=0.0)
	total_score = models.FloatField(default=0.0)

	created = models.DateTimeField()

	def __str__(self):
		return str(self.created)


class Settings(models.Model):
	max_money = models.IntegerField(default=1000, blank=True, null=True)
	finish_code = models.CharField(max_length=50)
