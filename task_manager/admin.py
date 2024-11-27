from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from task_manager.models import (
	TaskType,
	Position,
	Worker,
	Task,
)


@admin.register(Worker)
class WorkerAdmin(UserAdmin):
	list_display = UserAdmin.list_display + ("position",)
	list_editable = ["position"]
	fieldsets = UserAdmin.fieldsets + (
		(("Position", {
			"classes": ("wide", "collapse",),
			"fields": ("position",),
		}),)
	)
	add_fieldsets = UserAdmin.add_fieldsets + (
		(
			(
				"Details",
				{
					"fields": (
						"position",
						"first_name",
						"last_name",
					)
				},
			),
		)
	)
	search_fields = ("username", "first_name", "last_name")
	list_filter = ("position",)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
	list_display = (
		"name",
		"created_at",
		"deadline",
		"is_completed",
		"priority",
		"task_type",
	)
	list_editable = ["priority", "task_type"]
	search_fields = ("name",)
	list_filter = (
		"created_at",
		"deadline",
		"is_completed",
		"priority",
		"task_type",
		"assignees"
	)
	filter_horizontal = ("assignees",)


admin.site.register(Position)
admin.site.register(TaskType)
