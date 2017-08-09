from django import template

register = template.Library()


def num_range(num):
	return range(num)


register.filter('num_range', num_range)
