from django import forms
from .models import Task
from .models import Worker


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


class WorkerForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput, required=False)
	
	class Meta:
		model = Worker
		fields = (
			"username",
			"first_name",
			"last_name",
			"email",
			"position",
			"password",
		)
		widgets = {
			"username": forms.TextInput(
				attrs={
					"class": "form-control",
					"placeholder": "Enter your username",
					"autocomplete": "new-username"
				}
			),
			"first_name": forms.TextInput(
				attrs={
					"class": "form-control",
					"placeholder": "Enter your first name"
				}
			),
			"last_name": forms.TextInput(
				attrs={
					"class": "form-control",
					"placeholder": "Enter your last name"
				}
			),
			"email": forms.EmailInput(
				attrs={
					"class": "form-control", "placeholder": "Enter your email"
				}
			),
			"position": forms.RadioSelect(),
			"password": forms.PasswordInput(
				attrs={
					"class": "form-control",
					"placeholder": "Enter secure password",
					"autocomplete": "new-password"
				}
			),
		}
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		if not self.instance.pk:
			self.fields['password'].required = True
	
	def clean(self):
		cleaned_data = super().clean()
		
		if not self.instance.pk and not cleaned_data.get('password'):
			self.add_error('password', 'This field is required for new users.')
		
		return cleaned_data
