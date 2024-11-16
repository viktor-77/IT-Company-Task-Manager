from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase
from task_manager.models import Position


class PositionTestCase(TestCase):

    def setUp(self):
        Position.objects.create(name="Developer")

    def test_name_max_length(self):
        long_name = "x" * 101
        task_type = Position(name=long_name)

        with self.assertRaises(ValidationError):
            task_type.full_clean()

    def test_unique_name(self):
        with self.assertRaises(IntegrityError):
            Position.objects.create(name="Developer")

    def test_ordering(self):
        Position.objects.create(name="Refactoring")
        Position.objects.create(name="Feature")
        task_types = Position.objects.all()
        names = [task_type.name for task_type in task_types]

        self.assertEqual(names, ['Developer', 'Feature', "Refactoring"])

    def test_str_method(self):
        task_type = Position.objects.get(name="Developer")
        self.assertEqual(str(task_type), "Developer")
