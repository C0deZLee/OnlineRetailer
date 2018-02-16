from django.contrib import admin

from .models import Product


class ProductAdmin(admin.ModelAdmin):
	list_display = ['title', 'experiment_num', 'fake_quality', 'real_quality', 'verified_quality', 'price']


admin.site.register(Product, ProductAdmin)
