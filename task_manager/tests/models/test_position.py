from django.core.exceptions import ValidationError
from django.test import TestCase

from task_manager.models import Position
from task_manager.tests.models.utils import get_name_over_length_limit


class PositionTestCase(TestCase):
	
	def setUp(self):
		self.position = Position.objects.create(name="Developer")
	
	def test_name_max_length_validation_on_create(self):
		with self.assertRaises(ValidationError):
			Position.objects.create(name=get_name_over_length_limit())
	
	def test_name_max_length_validation_on_update(self):
		self.position.name = get_name_over_length_limit()
		
		with self.assertRaises(ValidationError):
			self.position.save()
	
	def test_unique_name_validation_on_create(self):
		with self.assertRaises(ValidationError):
			Position.objects.create(name=self.position.name)
	
	def test_unique_name_validation_on_update(self):
		test_position = Position.objects.create(name="Manager")
		test_position.name = self.position.name
		
		with self.assertRaises(ValidationError):
			test_position.save()
	
	def test_ascending_ordering(self):
		Position.objects.create(name="Manager")
		Position.objects.create(name="Analyst")
		names_list = list(Position.objects.values_list("name", flat=True))
		
		self.assertEqual(names_list, sorted(names_list))
	
	def test_str_method(self):
		self.assertEqual(str(self.position), self.position.name)
