from django.core.exceptions import ValidationError
from django.test import TestCase

from task_manager.models import TaskType
from task_manager.tests.models.utils import get_name_over_limit


class TaskTypeTestCase(TestCase):
	
	def setUp(self):
		self.task_type = TaskType.objects.create(name="Bug")
	
	def test_name_max_length_validation_on_create(self):
		with self.assertRaises(ValidationError):
			TaskType.objects.create(name=get_name_over_limit())
	
	def test_name_max_length_validation_on_update(self):
		self.task_type.name = get_name_over_limit()
		
		with self.assertRaises(ValidationError):
			self.task_type.save()
	
	def test_unique_name_validation_on_create(self):
		with self.assertRaises(ValidationError):
			TaskType.objects.create(name=self.task_type.name)
	
	def test_unique_name_validation_on_update(self):
		test_task_type = TaskType.objects.create(name="Refactoring")
		test_task_type.name = self.task_type.name
		
		with self.assertRaises(ValidationError):
			test_task_type.save()
	
	def test_ascending_ordering(self):
		TaskType.objects.create(name="Refactoring")
		TaskType.objects.create(name="Feature")
		names_list = list(TaskType.objects.values_list("name", flat=True))
		
		self.assertEqual(names_list, sorted(names_list))
	
	def test_str_method(self):
		self.assertEqual(str(self.task_type), self.task_type.name)
