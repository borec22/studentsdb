from django import template

register = template.Library()

@register.filter
def nice_username(user):
	"""recive object User and return username"""
	
	if user.first_name and user.last_name:
		obj = user.get_full_name()
	else:
		obj = user.username
	return obj