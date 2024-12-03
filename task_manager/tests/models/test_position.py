from django.core.exceptions import ValidationError
from django.test import TestCase

from task_manager.models import Position


class PositionTestCase(TestCase):
	
	def setUp(self):
		self.position = Position.objects.create(name="Developer")
	
	def test_name_max_length(self):
		long_name = "x" * 101
		
		with self.assertRaises(ValidationError):
			Position.objects.create(name=long_name)
	
	def test_unique_name(self):
		with self.assertRaises(ValidationError):
			Position.objects.create(name=self.position.name)
	
	def test_ascending_ordering(self):
		Position.objects.create(name="Manager")
		Position.objects.create(name="Analyst")
		names = [position.name for position in Position.objects.all()]
		
		self.assertEqual(names, sorted(names))
	
	def test_str_method(self):
		self.assertEqual(str(self.position), self.position.name)
