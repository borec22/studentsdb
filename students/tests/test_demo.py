from django.test import TestCase


class DemoTest(TestCase):

	def test_demo(self):
		self.assertEqual(3, 2+1)

	def test_demo_fail(self):
		self.assertEqual('serhii', 'serhii')
