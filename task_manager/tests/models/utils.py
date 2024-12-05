from task_manager.models import Position, TaskType


def get_name_over_length_limit(length_limit: int = 101) -> str:
	return "x" * length_limit


def create_position(name: str) -> Position:
	return Position.objects.create(name=name)


def create_task_type(name: str) -> Position:
	return TaskType.objects.create(name=name)
