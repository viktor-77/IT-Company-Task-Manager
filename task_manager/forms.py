from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from task_manager.models import Task
from task_manager.validators import field_min_length_validator


class TaskForm(forms.ModelForm):
	priority = forms.ChoiceField(
		choices=Task.PRIORITY_CHOICES,
		widget=forms.RadioSelect(
			attrs={"class": "form-check-input"}
		)
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
			"assignees",
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
			"is_completed": forms.CheckboxInput(
				attrs={"class": "form-check-input"}
			),
			"task_type": forms.RadioSelect(),
			"assignees": forms.SelectMultiple(attrs={"class": "form-select"})
		}


class WorkerBaseForm(forms.ModelForm):
	username = forms.CharField(
		widget=forms.TextInput(
			attrs={
				"class": "form-control",
				"placeholder": "Enter your username",
				"autocomplete": "new-username",
			}
		),
		validators=[field_min_length_validator()]
	)
	first_name = forms.CharField(
		widget=forms.TextInput(
			attrs={
				"class": "form-control",
				"placeholder": "Enter your first name",
			}
		),
		validators=[field_min_length_validator()]
	)
	last_name = forms.CharField(
		widget=forms.TextInput(
			attrs={
				"class": "form-control",
				"placeholder": "Enter your last name",
			}
		),
		validators=[field_min_length_validator()]
	)
	
	def clean_password(self):
		if password := self.cleaned_data.get('password'):
			try:
				validate_password(password, self.instance)
			except ValidationError as e:
				self.add_error('password', e)
		return password


class MetaBaseForm:
	model = get_user_model()
	fields = (
		"username",
		"first_name",
		"last_name",
		"email",
		"position",
		"password",
	)
	widgets = {
		"email": forms.EmailInput(
			attrs={
				"class": "form-control",
				"placeholder": "Enter your email",
			}
		),
		"position": forms.RadioSelect(),
		"password": forms.PasswordInput(
			attrs={
				"class": "form-control",
				"placeholder": "Enter your password",
				"autocomplete": "new-password",
			}
		)
	}


class WorkerCreateForm(WorkerBaseForm):
	class Meta(MetaBaseForm):
		pass


class WorkerUpdateForm(WorkerBaseForm):
	password = forms.CharField(
		required=False,
		widget=MetaBaseForm.widgets['password'],
	)
	
	class Meta(MetaBaseForm):
		fields = (
			"username",
			"first_name",
			"last_name",
			"email",
			"password",
		)


class SearchForm(forms.Form):
	query = forms.CharField(
		max_length=100,
		label="",
		widget=forms.TextInput(
			attrs={"placeholder": "Search...", "class": "form-control"}
		)
	)
