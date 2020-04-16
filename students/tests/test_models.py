from django.test import TestCase

from students.models.students_model import Student
from students.models.groups_model import Group 
from students.models.exams_model import Exam  


class ModelTests(TestCase):
	"""Test models"""

	def test_unicode(self):
		student = Student(first_name='Demo', last_name='Student')
		self.assertEqual(unicode(student), u'Demo Student')

		group = Group(title='Demo_group')
		self.assertEqual(unicode(group), u'Demo_group')

		exam = Exam(subject='Demo_exam')
		self.assertEqual(unicode(exam), u'Demo_exam ')