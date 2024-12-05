import datetime

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from task_manager.models import Task
from task_manager.tests.models.utils import (
	create_task_type,
	get_name_over_length_limit,
)


class TaskModelTest(TestCase):
	ACTUAL_DEADLINE = datetime.date.today() + datetime.timedelta(days=1)
	PAST_DEADLINE = datetime.date.today() - datetime.timedelta(days=1)
	
	def setUp(self):
		self.task_type = create_task_type("Bug")
		self.task = self._create_task(name="base_task")
	
	def test_name_max_length_validation_on_create(self):
		with self.assertRaises(ValidationError):
			self._create_task(name=get_name_over_length_limit())
	
	def test_name_max_length_validation_on_update(self):
		self.task.name = get_name_over_length_limit()
		
		with self.assertRaises(ValidationError):
			self.task.save()
	
	def test_unique_name_validation_on_create(self):
		with self.assertRaises(ValidationError):
			self._create_task(name=self.task.name)
	
	def test_unique_name_validation_on_update(self):
		test_task = self._create_task()
		test_task.name = self.task.name
		
		with self.assertRaises(ValidationError):
			test_task.save()
	
	def test_past_deadline_validation_on_create(self):
		with self.assertRaises(ValidationError) as context:
			self._create_task(deadline=self.PAST_DEADLINE)
		
		self.assertRaisesMessage(
			context, Task.DEADLINE_ERROR_MESSAGE
		)
	
	def test_past_deadline_validation_on_update(self):
		self.task.deadline = self.PAST_DEADLINE
		
		with self.assertRaises(ValidationError) as context:
			self.task.save()
		
		self.assertRaisesMessage(
			context, Task.DEADLINE_ERROR_MESSAGE
		)
	
	def test_is_completed_field_set_false_by_default(self):
		self.assertFalse(self.task.is_completed)
	
	def test_task_not_create_without_task_type(self):
		with self.assertRaises(ValidationError):
			Task.objects.create(
				name="test-name",
				description="description",
				deadline=self.ACTUAL_DEADLINE,
				priority=1,
			)
	
	def test_task_type_sets_null_on_delete(self):
		self.task_type.delete()
		self.task.refresh_from_db()
		
		self.assertTrue(self.task)
		self.assertIsNone(self.task.task_type)
	
	def test_task_assignees_adding(self):
		user = get_user_model().objects.create_user(
			username="test-user", password="test-password",
		)
		self.task.assignees.add(user)
		
		self.assertIn(user, self.task.assignees.all())
	
	def test_str_method(self):
		self.assertEqual(str(self.task), self.task.name)
	
	def _create_task(
		self,
		name: str = "test-name",
		description: str = "test-description",
		deadline: datetime.date = None,
		priority: int = 3,
	) -> Task:
		if deadline is None:
			deadline = self.ACTUAL_DEADLINE
		
		return Task.objects.create(
			name=name,
			description=description,
			deadline=deadline,
			priority=priority,
			task_type=self.task_type,
		)
