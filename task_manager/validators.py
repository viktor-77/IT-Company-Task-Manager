from django.core.validators import MinLengthValidator


def get_min_length_validator(min_length=5):
	return MinLengthValidator(
		min_length,
		message=f"This field must be at least {min_length} characters long."
	)
