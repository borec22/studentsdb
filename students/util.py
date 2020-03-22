from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.translation import ugettext as _
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

class DispatchLoginRequired(object):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        # Try to dispatch to the right method; if a method doesn't exist,
        # defer to the error handler. Also defer to the error handler if the
        # request method isn't on the approved list.
        if request.method.lower() in self.http_method_names:
            handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)



def get_language_from_request(request):
	if request.COOKIES.get('django_language') == 'en':
		return 'en'
	elif request.COOKIES.get('django_language') == 'uk':
		return _(u'uk')
	else:
		return none
	

def get_current_group(request):
	"""Returns currently selected group or None"""

	# we remember selected group in a cookie
	#import pdb; pdb.set_trace()
	language = request.COOKIES.get('django_language')
	pk = request.COOKIES.get('current_group')

	if pk:
		from students.models.groups_model import Group
		try:
			group = Group.objects.get(pk=int(pk))
		except Group.DoesNotExist:
			return None
		else:
			return group
	else:
		return None

def get_groups(request):
	"""Returns list of existing groups"""
	# deferred import of Group model to avoid cycled imports
	from students.models.groups_model import Group

	# get currently selected group
	cur_group = get_current_group(request)

	groups = []
	for group in Group.objects.all().order_by('title'):
		groups.append({
			'id': group.id,
			'title': group.title,
			'leader': group.leader and (u'%s %s' %(group.leader.first_name, \
				                       group.leader.last_name)) or None,
			'selected': cur_group and cur_group.id == group.id and True or False
		})
	return groups


def paginate(objects, size, request, context, var_name='object_list'):
	"""Paginate objects provided by view.

	This function takes:
	   * list of elements;
	   * number of objects per page;
	   * request object to get url parameters from;
	   * contaxt to set new variables into;
	   * var_name - variable name for list of obects.

	It returns updated context object.
	"""
	# apply pagination
	paginator = Paginator(objects, size)

	# try to get page number from request
	page = request.GET.get('page', '1')
	try:
		object_list = paginator.page(page)
	except PageNotAnInteger:
		# if page is not an integer, deliver first page
		object_list = paginator.page(1)
	except EmptyPage:
		# if page is out of range (e.g. 9999),
		# deliver last page of results
		object_list = paginator.page(paginator.num_pages)

	# set variabels into context
	context[var_name] = object_list
	context['is_paginated'] = object_list.has_other_pages()
	context['page_obj'] = object_list
	context['paginator'] = paginator

	return context
