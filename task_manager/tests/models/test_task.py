import datetime

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from task_manager.models import Task, TaskType, Position


class TaskModelTest(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="Developer")
        self.task_type = TaskType.objects.create(name="Bug")
        self.worker = get_user_model().objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpassword",
            position_id=self.position.id,
        )
        self.task = Task.objects.create(
            name="Task Name",
            description="Some description.",
            deadline=datetime.date.today() + datetime.timedelta(days=7),
            is_completed=False,
            priority=3,
            task_type=self.task_type,
        )

    def test_name_max_length(self):
        long_name = "x" * 101
        self.task.name = long_name

        with self.assertRaises(ValidationError):
            self.task.full_clean()

    def test_clean_deadline_with_past_date(self):
        past_date = datetime.date.today() - datetime.timedelta(days=1)
        task = Task(
            name="Past Deadline Task",
            description="Task with past deadline.",
            deadline=past_date,
            is_completed=False,
            priority=2,
            task_type=self.task_type,
        )
        with self.assertRaises(ValidationError) as context:
            task.clean_deadline()

        self.assertEqual(
            context.exception.messages[0],
            "The deadline cannot be in the past."
        )

    def test_str_method(self):
        self.assertEqual(str(self.task), self.task.name)
