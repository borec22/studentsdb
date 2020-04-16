from datetime import datetime

from django.test import TestCase, Client
from django.core.urlresolvers import reverse

from students.models.students_model import Student
from students.models.groups_model import Group


class TestStudentList(TestCase):

	def setUp(self):
		# create groups
		group1, created = Group.objects.get_or_create(
			title="MtM-1")
		group2, created = Group.objects.get_or_create(
			title="MtM-2")

		# create 4 students: 1 for group1 and 3 for group2
		Student.objects.get_or_create(
			first_name="Vitaliy",
			last_name="Podoba",
			birthday=datetime.today(),
			ticket="12345",
			student_group=group1)
		Student.objects.get_or_create(
			first_name="John",
			last_name="Dobson",
			birthday=datetime.today(),
			ticket="23456",
			student_group=group2)
		Student.objects.get_or_create(
			first_name="Sam",
			last_name="Stefenson",
			birthday=datetime.today(),
			ticket="34567",
			student_group=group2)
		Student.objects.get_or_create(
			first_name="Arnpld",
			last_name="Kidney",
			birthday=datetime.today(),
			ticket="45678",
			student_group=group2)

		# remember test browser
		self.client = Client()

		# remember url to our homepage
		self.url = reverse('home')

	def test_students_list(self):
		# make request to the server to get homepage
		response = self.client.get(self.url)

		# have we received OK status from the server?
		self.assertEqual(response.status_code, 200)

		# do we have student name on a page?
		self.assertIn('Vitaliy', response.content)

		import pdb; pdb.set_trace()

		# ensure we got 3 students, pagination limit is 3
		self.assertEqual(len(response.context['students']), 3)

	def test_current_group(self):
		# set group1 as currently selected group
		group = Group.objects.filter(title="MtM-1")[0]
		self.client.cookies['current_group'] = group.id

		# make request to server to get homepage page
		response = self.client.get(self.url)

		# in group1 we have only one student
		self.assertEqual(len(response.context['students']), 1)

	def test_order_by(self):
		# set order by Last Name
		response = self.client.get(self.url, {'order_by': 'last_name'})

		# now check if we got proper order
		students = response.context['students']
		self.assertEqual(students[0].last_name, 'Dobson')
		self.assertEqual(students[1].last_name, 'Kidney')
		self.assertEqual(students[2].last_name, 'Podoba')

	def test_reverse(self):
		# set order by Last Name and parameter reverse
		response = self.client.get(self.url, {'order_by': 'last_name', 'reverse': '1'})

		# now check if we got proper order
		students = response.context['students']
		self.assertEqual(students[0].last_name, 'Stefenson')
		self.assertEqual(students[1].last_name, 'Podoba')
		self.assertEqual(students[2].last_name, 'Kidney')

	def test_pagination(self):
		# navigate with second page with students
		response = self.client.get(self.url, {'page': '2'})

		self.assertEqual(len(response.context['students']), 1)
		self.assertEqual(response.context['is_paginated'], True)
		self.assertEqual(response.context['students'][0].last_name, 'Stefenson') 

