from django import forms
from .models import Task


class TaskForm(forms.ModelForm):
	priority = forms.ChoiceField(
		choices=Task.PRIORITY_CHOICES,
		widget=forms.RadioSelect,
	)
	
	class Meta:
		model = Task
		fields = [
			"name",
			"description",
			"deadline",
			"is_completed",
			"priority",
			"task_type",
			"assignees"
		]
		widgets = {
			"name": forms.TextInput(
				attrs={
					"class": "form-control",
					"placeholder": "Enter task name"
				}
			),
			"description": forms.Textarea(
				attrs={
					"class": "form-control", "rows": 5,
					"placeholder": "Enter task description"
				}
			),
			"deadline": forms.DateInput(
				attrs={"class": "form-control", "type": "date"}
			),
			"task_type": forms.RadioSelect(),
			"assignees": forms.SelectMultiple(attrs={"class": "form-select"})
		}
