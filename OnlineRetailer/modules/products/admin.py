from django.contrib import admin

from .models import Product


class ProductAdmin(admin.ModelAdmin):
	list_display = ['title', 'fake_quality', 'real_quality','verified_quality','price']


admin.site.register(Product, ProductAdmin)
