import datetime

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from task_manager.models import Task, TaskType
from task_manager.tests.models.utils import get_name_over_length_limit


class TaskModelTest(TestCase):
	TEST_NAME = "test-name"
	DESCRIPTION = "description"
	PRIORITY = 3
	ACTUAL_DEADLINE = datetime.date.today() + datetime.timedelta(days=7)
	PAST_DEADLINE = datetime.date.today() - datetime.timedelta(days=7)
	
	def setUp(self):
		self.task_type = TaskType.objects.create(name="Bug")
		self.task = Task.objects.create(
			name="task-name",
			description=self.DESCRIPTION,
			deadline=self.ACTUAL_DEADLINE,
			priority=self.PRIORITY,
			task_type=self.task_type,
		)
	
	def test_name_max_length_validation_on_create(self):
		with self.assertRaises(ValidationError):
			Task.objects.create(
				name=get_name_over_length_limit(),
				description=self.DESCRIPTION,
				deadline=self.ACTUAL_DEADLINE,
				priority=self.PRIORITY,
				task_type=self.task_type,
			)
	
	def test_name_max_length_validation_on_update(self):
		self.task.name = get_name_over_length_limit()
		
		with self.assertRaises(ValidationError):
			self.task.save()
	
	def test_unique_name_validation_on_create(self):
		with self.assertRaises(ValidationError):
			Task.objects.create(
				name=self.task.name,
				description=self.DESCRIPTION,
				deadline=self.ACTUAL_DEADLINE,
				priority=self.PRIORITY,
				task_type=self.task_type,
			)
	
	def test_unique_name_validation_on_update(self):
		test_task = Task.objects.create(
			name=self.TEST_NAME,
			description=self.DESCRIPTION,
			deadline=self.ACTUAL_DEADLINE,
			priority=self.PRIORITY,
			task_type=self.task_type,
		)
		test_task.name = self.task.name
		
		with self.assertRaises(ValidationError):
			test_task.save()
	
	def test_past_deadline_validation_on_create(self):
		with self.assertRaises(ValidationError) as context:
			Task.objects.create(
				name=self.TEST_NAME,
				description=self.DESCRIPTION,
				deadline=self.PAST_DEADLINE,
				priority=self.PRIORITY,
				task_type=self.task_type,
			)
		
		self.assertIn(
			Task.DEADLINE_ERROR_MESSAGE, context.exception.messages,
		)
	
	def test_past_deadline_validation_on_update(self):
		self.task.deadline = self.PAST_DEADLINE
		
		with self.assertRaises(ValidationError) as context:
			self.task.save()
		
		self.assertIn(
			Task.DEADLINE_ERROR_MESSAGE, context.exception.messages,
		)
	
	def test_is_completed_field_set_false_by_default(self):
		self.assertFalse(self.task.is_completed)
	
	def test_str_method(self):
		self.assertEqual(str(self.task), self.task.name)
