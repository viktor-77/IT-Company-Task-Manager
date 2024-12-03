from django.test import TestCase
from django.contrib.auth import get_user_model

from task_manager.models import Position


class WorkerTestCase(TestCase):
	
	def setUp(self):
		self.position = Position.objects.create(name="Developer")
		self.user = get_user_model().objects.create_user(
			username="andriy",
			password="test-password",
			position=self.position,
		)
	
	def test_creation_worker_without_position(self):
		user = get_user_model().objects.create_user(
			username="test-user", password="test-password",
		)
		
		self.assertEqual(user.username, "test-user")
		self.assertIsNone(user.position)
	
	def test_position_sets_none_on_delete(self):
		self.position.delete()
		self.user.refresh_from_db()
		
		self.assertIsNone(self.user.position)
	
	def test_ascending_ordering(self):
		get_user_model().objects.create_user(
			username="vasil", password="vasil-password",
		)
		get_user_model().objects.create_user(
			username="ivan", password="ivan-password",
		)
		usernames = [user.username for user in get_user_model().objects.all()]
		
		self.assertEqual(usernames, sorted(usernames))
	
	def test_str_method(self):
		self.assertEqual(str(self.user), self.user.username)
