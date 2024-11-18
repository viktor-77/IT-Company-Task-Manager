from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

from task_manager.models import Position


class PositionTestCase(TestCase):

    def setUp(self):
        Position.objects.create(name="Developer")

    def test_name_max_length(self):
        long_name = "x" * 101
        position = Position(name=long_name)

        with self.assertRaises(ValidationError):
            position.full_clean()

    def test_unique_name(self):
        with self.assertRaises(IntegrityError):
            Position.objects.create(name="Developer")

    def test_ordering(self):
        Position.objects.create(name="Refactoring")
        Position.objects.create(name="Feature")
        positions = Position.objects.all()
        names = [position.name for position in positions]

        self.assertEqual(names, ['Developer', 'Feature', "Refactoring"])

    def test_str_method(self):
        position = Position.objects.get(name="Developer")
        self.assertEqual(str(position), "Developer")
