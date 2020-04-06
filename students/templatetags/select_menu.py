from django import template
from django.urls import resolve

register = template.Library()

# Usage: {% select_menu 'groups' %}

@register.simple_tag(takes_context=True)
def select_menu(context, string):
	path = context.get('request').path
	resolvers = resolve(path).url_name
	if resolvers == string:
		return 'class="active"'
	else:
		return ''
