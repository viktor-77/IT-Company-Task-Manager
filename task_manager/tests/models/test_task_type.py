from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

from task_manager.models import TaskType


class TaskTypeTestCase(TestCase):

    def setUp(self):
        TaskType.objects.create(name="Bug")

    def test_name_max_length(self):
        long_name = "x" * 101
        task_type = TaskType(name=long_name)

        with self.assertRaises(ValidationError):
            task_type.full_clean()

    def test_unique_name(self):
        with self.assertRaises(IntegrityError):
            TaskType.objects.create(name="Bug")

    def test_ordering(self):
        TaskType.objects.create(name="Refactoring")
        TaskType.objects.create(name="Feature")
        task_types = TaskType.objects.all()
        names = [task_type.name for task_type in task_types]

        self.assertEqual(names, ['Bug', 'Feature', "Refactoring"])

    def test_str_method(self):
        task_type = TaskType.objects.get(name="Bug")
        self.assertEqual(str(task_type), "Bug")
