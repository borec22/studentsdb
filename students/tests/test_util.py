from datetime import datetime

from django.utils.translation import ugettext as _
from django.test import TestCase
from django.http import HttpRequest

from students.models.students_model import Student
from students.models.groups_model import Group
from students.util import get_current_group, get_groups, paginate, get_language_from_request


class UtilsTestCase(TestCase):
	"""Test functions from util module"""

	def setUp(self):
	    # create 2 groups
	    group1, created = Group.objects.get_or_create(
	    	id=1,
	    	title="Group1")
	    group2, created = Group.objects.get_or_create(
	    	id=2,
	    	title="Group2")
	    # created student
	    student, created = Student.objects.get_or_create(
	    	id=1,
	    	first_name="Serhii",
	    	last_name="Romanchuk",
	    	birthday=datetime.today(),
	    	ticket='12345')

	    # set student as leader for group1
	    group1.leader = student
	    group1.save()

	def test_get_current_group(self):
	    # prepare request object to pass to utility function
	    request = HttpRequest()

	    #test with no group set in cookie
	    request.COOKIES['current_group'] = ''
	    self.assertEqual(None, get_current_group(request))

	    #test with invalid group id
	    request.COOKIES['current_group'] = '12345'
	    self.assertEqual(None, get_current_group(request))

	    #test with proper group identificator
	    group = Group.objects.filter(title="Group1")[0]
	    request.COOKIES['current_group'] = str(group.id)
	    self.assertEqual(group, get_current_group(request))

	def test_get_groups(self):
		# prepare test request with selected group
		request = HttpRequest()
		request.COOKIES['current_group'] = '2'

		# check get groups list
		self.assertEqual(get_groups(request), [
			{'leader': u'Serhii Romanchuk',
			 'selected': False,
			 'title': u'Group1',
			 'id': 1},
			{'leader': None,
			 'selected': True,
			 'title': u'Group2',
			 'id': 2}
		])

	def test_paginate(self):
		# this diractionary will serve as template context
		context = {}

		# prepare test request
		request = HttpRequest()

		# check PageNotAnInteger case: ab string
		request.GET['page'] = 'ab'
		result = paginate([1, 2, 3, 4], 3, request, context, 
			var_name = 'object_list')
		self.assertEqual(len(result['object_list']), 3)
		self.assertEqual(result['is_paginated'], True)
		self.assertEqual(len(result['page_obj']), 3)
		self.assertEqual(result['object_list'][0], 1)
		self.assertEqual(result['object_list'][1], 2)
		self.assertEqual(result['object_list'][2], 3)

		# check empty page case: should be last page
		request.GET['page'] = '9999'
		result = paginate([1, 2, 3, 4], 3, request, context, 
			var_name = 'object_list')
		self.assertEqual(len(result['object_list']), 1)
		self.assertEqual(result['object_list'][0], 4)



		# check valid page: second page
		request.GET['page'] = '2'
		result = paginate([1, 2, 3, 4, 5], 3, request, context, 
			var_name = 'my_list')
		self.assertEqual(len(result['my_list']), 2)
		self.assertEqual(result['my_list'][0], 4)
		self.assertEqual(result['my_list'][1], 5)

	def test_get_language_from_request(self):
		# prepare test request to pass to utility function
		request = HttpRequest()

		# test with no language set in cookie
		request.COOKIES['django_language'] = ''
		self.assertEqual(_(u'uk'), get_language_from_request(request))

		# test with invalid cookie
		request.COOKIES['django_language'] = 'qaz'
		self.assertEqual(_(u'uk'), get_language_from_request(request))

		# test with proper cookie
		request.COOKIES['django_language'] = 'en'
		self.assertEqual('English', get_language_from_request(request))



