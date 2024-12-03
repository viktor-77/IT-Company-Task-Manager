from django.core.exceptions import ValidationError
from django.test import TestCase

from task_manager.models import TaskType


class TaskTypeTestCase(TestCase):
	
	def setUp(self):
		self.task_type = TaskType.objects.create(name="Bug")
	
	def test_name_max_length(self):
		long_name = "x" * 101
		
		with self.assertRaises(ValidationError):
			TaskType.objects.create(name=long_name)
	
	def test_unique_name(self):
		with self.assertRaises(ValidationError):
			TaskType.objects.create(name=self.task_type.name)
	
	def test_ascending_ordering(self):
		TaskType.objects.create(name="Refactoring")
		TaskType.objects.create(name="Feature")
		names = [task_type.name for task_type in TaskType.objects.all()]
		
		self.assertEqual(names, sorted(names))
	
	def test_str_method(self):
		self.assertEqual(str(self.task_type), self.task_type.name)
