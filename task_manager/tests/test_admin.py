from django.contrib.admin import site
from django.contrib.auth import get_user_model
from django.test import SimpleTestCase, TestCase
from django.urls import reverse

from task_manager.admin import TaskAdmin, WorkerAdmin
from task_manager.models import Position, Task


class WorkerAdminTest(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="Developer")
        self.user = get_user_model().objects.create_superuser(
            username="testuser",
            email="test@example.com",
            password="testpassword",
            position_id=self.position.id,
        )

        self.client.force_login(self.user)
        self.admin = WorkerAdmin(get_user_model(), site)

    def test_list_display_includes_position(self):
        self.assertIn("position", self.admin.list_display)

    def test_fieldsets_includes_position_field(self):
        url = reverse("admin:task_manager_worker_change", args=[self.user.id])
        response = self.client.get(url)

        self.assertContains(response, "position")

    def test_add_fieldsets_contains_position_field(self):
        url = reverse("admin:task_manager_worker_add")
        response = self.client.get(url)

        self.assertContains(response, "position")

    def test_search_fields_are_correct(self):
        self.assertEqual(
            self.admin.search_fields, ("username", "first_name", "last_name")
        )

    def test_list_filter_includes_position(self):
        self.assertEqual(self.admin.list_filter, ("position",))


class TaskAdminTest(SimpleTestCase):
    def setUp(self):
        self.admin = TaskAdmin(Task, site)

    def test_list_display_is_correct(self):
        self.assertEqual(
            self.admin.list_display,
            ("name", "deadline", "is_completed", "priority", "task_type"),
        )

    def test_search_fields_are_correct(self):
        self.assertEqual(self.admin.search_fields, ("name",))

    def test_list_filter_is_correct(self):
        self.assertEqual(
            self.admin.list_filter,
            ("deadline", "is_completed", "priority", "task_type", "assignees"),
        )
