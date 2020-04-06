from django import template

register = template.Library()

# Usage: {% pagenav object_list=students is_paginated=is_paginated paginator=paginator %}

#@register.simple_tag()
@register.simple_tag
def pagenav(*args, **kwargs):
	t = template.loader.get_template('students/pagination.html')
	return t.render(template.Context({
		'object_list': kwargs['object_list'],
		'is_paginated': kwargs['is_paginated'],
		'paginator': kwargs['paginator']}
	))
