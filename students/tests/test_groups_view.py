from django.test import TestCase, Client, override_settings
from django.core.urlresolvers import reverse

@override_settings(LANGUAGE_CODE='en')
class TestGroupsList(TestCase):

	fixtures = ['students_test_data.json']

	def setUp(self):
		self.client = Client()
		self.url = reverse('groups')

	def test_groups_list(self):

		self.client.login(username='admin', password='admin')
		response = self.client.get(self.url)

		self.assertEqual(response.status_code, 200)
		self.assertIn('Group1', response.content)
		self.assertEqual(len(response.context['groups']), 2)

	def test_order_by_and_reverse(self):

		self.client.login(username='admin', password='admin')
		response = self.client.get(self.url, {'order_by': 'title'})

		groups = response.context['groups']
		self.assertEqual(groups[0].title, 'Group1')
		self.assertEqual(groups[1].title, 'Group2')

		response = self.client.get(self.url, {'order_by': 'title', 'reverse': '1'})
		groups = response.context['groups']
		self.assertEqual(groups[0].title, 'Group2')
		self.assertEqual(groups[1].title, 'Group1')

	def test_pagination(self):

		self.client.login(username='admin', password='admin')
		response = self.client.get(self.url, {'page': '1'})
		self.assertEqual(len(response.context['groups']), 2)
		self.assertEqual(response.context['is_paginated'], False)







