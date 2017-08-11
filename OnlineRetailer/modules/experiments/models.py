from django.db import models


class Record(models.Model):
    purchases = models.ManyToManyField('Purchase')

    product = models.ForeignKey('products.Product')
    created = models.DateTimeField()
    score = models.FloatField(default=0.0)

    def __str__(self):
        return str(self.created)


class Purchase(models.Model):
    products = models.ForeignKey('products.Product')
    amount = models.IntegerField(default=1)

    def __str__(self):
        return self.products.title + ' x' + str(self.amount)


class Settings(models.Model):
    max_money = models.IntegerField(default=1000, blank=True, null=True)
    finish_code = models.CharField(max_length=50)
