from django import template

register = template.Library()


def divide_by(num1, num2):
	return float(num1)/float(num2)


register.filter('divide_by', divide_by)
