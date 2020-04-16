import logging

from django.utils.six import StringIO
from django.test import TestCase

from students.models.students_model import Student
from students.models.groups_model import Group
from students.models.exams_model import Exam
from students import signals


class StudentSignalsTests(TestCase):

	def test_log_student_updated_added_event(self):
		"""Check logging signal for newly created student"""
		
		# add own root handler to catch student signals output
		out = StringIO()
		handler = logging.StreamHandler(out)
		logging.root.addHandler(handler)

		# now create student, this should raise new message 
		# inside logger outputfile
		student = Student(first_name='Demo', last_name='Student')
		student.save()

		# check output file content
		out.seek(0)
		self.assertEqual(out.readlines()[-1],
			'Student added: Demo Student (ID: %d)\n' % student.id)

		# now update existing student and check last line in out
		student.ticket = '12345'
		student.save()
		out.seek(0)
		self.assertEqual(out.readlines()[-1],
			'Student updated: Demo Student (ID: %d)\n' % student.id)

		# remove our handler from root logger
		logging.root.removeHandler(handler)

	def test_log_group_updated_added_event(self):
		"""Check logging signal for newly created group"""

		# add own root handler to catch student signals output
		out = StringIO()
		handler = logging.StreamHandler(out)
		logging.root.addHandler(handler)

		# now create group, this should raise new message 
		# inside logger outputfile
		group = Group(title='Demo_group')
		group.save()

		# check output file content
		out.seek(0)
		self.assertEqual(out.readlines()[-1],
			'Group added: Demo_group (ID: %d)\n' % group.id)

		# now update existing group and check last line in out
		group.title = 'Demo'
		group.save()
		out.seek(0)
		self.assertEqual(out.readlines()[-1],
			'Group updated: Demo (ID: %d)\n' % group.id)

		# remove our handler from root logger
		logging.root.removeHandler(handler)

	def test_log_exam_updated_added_event(self):
		"""Check logging signal for newly created exam"""

		# add own root handler to catch exam signals output
		out = StringIO()
		handler = logging.StreamHandler(out)
		logging.root.addHandler(handler)

		# now create exam, this should raise new message 
		# inside logger outputfile
		exam = Exam(subject='Demo_exam')
		exam.save()

		# check output file content
		out.seek(0)
		self.assertEqual(out.readlines()[-1],
			'Exam added: Demo_exam (ID: %d)\n' % exam.id)

		# now update existing exam and check last line in out
		exam.subject = 'Demo'
		exam.save()
		out.seek(0)
		self.assertEqual(out.readlines()[-1],
			'Exam updated: Demo (ID: %d)\n' % exam.id)

		# remove our handler from root logger
		logging.root.removeHandler(handler)

	def test_log_deleted_event(self):
		"""Check logging signal when student has been deleted"""

		# add own root handler to catch student signal output
		out = StringIO()
		handler = logging.StreamHandler(out)
		logging.root.addHandler(handler)

		student = Student(first_name='First', last_name='Last')
		student.save()

		sid = student.id
		student.delete()

		out.seek(0)
		self.assertEqual(out.readlines()[-1],
			'Student deleted: First Last (ID: %d)\n' % sid)

		logging.root.removeHandler(handler)



