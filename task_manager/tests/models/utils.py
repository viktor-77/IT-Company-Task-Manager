from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser

from task_manager.models import Position, TaskType


def get_name_over_length_limit(length_limit: int = 101) -> str:
	return "x" * length_limit


def create_position(name: str) -> Position:
	return Position.objects.create(name=name)


def create_task_type(name: str) -> Position:
	return TaskType.objects.create(name=name)


def create_user() -> AbstractUser:
	return get_user_model().objects.create_user(
		username="test-user", password="test-password",
	)
