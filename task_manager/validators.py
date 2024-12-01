from django.core.validators import MinLengthValidator


def field_min_length_validator(min_length: int = 5) -> MinLengthValidator:
	return MinLengthValidator(
		min_length,
		message=f"This field must be at least {min_length} characters long."
	)
