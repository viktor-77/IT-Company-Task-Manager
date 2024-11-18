from django.test import TestCase
from django.contrib.auth import get_user_model

from task_manager.models import Position


class PositionTestCase(TestCase):

    def setUp(self):
        self.position = Position.objects.create(name="Developer")
        get_user_model().objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpassword",
            position_id=self.position.id,
        )

    def test_str_method(self):
        user = get_user_model().objects.get(username="testuser")
        self.assertEqual(str(user), user.username)
