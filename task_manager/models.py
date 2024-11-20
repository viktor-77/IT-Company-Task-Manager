from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.timezone import now


class TaskType(models.Model):
	name = models.CharField(max_length=100, unique=True)
	
	class Meta:
		ordering = ['name']
	
	def __str__(self) -> str:
		return self.name


class Position(models.Model):
	name = models.CharField(max_length=100, unique=True)
	
	class Meta:
		ordering = ['name']
	
	def __str__(self) -> str:
		return self.name


class Worker(AbstractUser):
	position = models.ForeignKey(Position, on_delete=models.CASCADE)
	email = models.EmailField(unique=True, blank=False, null=False)
	first_name = models.CharField(max_length=100, blank=False, null=False)
	last_name = models.CharField(max_length=100, blank=False, null=False)
	
	class Meta:
		verbose_name = 'Worker'
		verbose_name_plural = 'Workers'
	
	def __str__(self) -> str:
		return self.username


class Task(models.Model):
	PRIORITY_CHOICES = [
		(4, "Urgent"),
		(3, "High"),
		(2, "Medium"),
		(1, "Low"),
	]
	
	name = models.CharField(max_length=100, unique=True, db_index=True)
	description = models.TextField()
	created_at = models.DateField(auto_now_add=True)
	deadline = models.DateField()
	is_completed = models.BooleanField(default=False)
	priority = models.IntegerField(choices=PRIORITY_CHOICES)
	task_type = models.ForeignKey(TaskType, on_delete=models.CASCADE)
	assignees = models.ManyToManyField(Worker, related_name="tasks")

	def clean(self):
		if self.deadline and self.deadline < now().date():
			raise ValidationError(
				{"deadline": "The deadline cannot be in the past."}
			)
	
	def save(self, *args, **kwargs):
		self.full_clean()
		super().save(*args, **kwargs)
	
	def __str__(self) -> str:
		return self.name
	
	class Meta:
		ordering = ['-priority', 'deadline']
