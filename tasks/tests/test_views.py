from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone

from tasks.models import Tag, Task, TaskType

User = get_user_model()


class TaskListViewSet(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="user1",
            password="pass1234"
        )
        self.client.login(username="user1", password="pass1234")
        self.task_type = TaskType.objects.create(name="Bug Fix")
        self.deadline = timezone.now() + timedelta(days=7)
        self.task = Task.objects.create(
            name="Test Task",
            description="Users cannot login",
            deadline=self.deadline,
            priority=Task.Priority.HIGH,
            task_type=self.task_type,
            created_by=self.user
        )

    def test_task_list_view_status_code_and_template(self):
        response = self.client.get(reverse("tasks:task-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Task")
        self.assertTemplateUsed(response, "tasks/task_list.html")

    def test_task_detail_view(self):
        response = self.client.get(
            reverse(
                "tasks:task-detail",
                args=[self.task.id]
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Task")
        self.assertTemplateUsed(response, "tasks/task_detail.html")

    def test_task_list_view_search_match(self):
        Task.objects.create(
            name="Test Task 2",
            description="Users cannot login",
            deadline=self.deadline,
            priority=Task.Priority.HIGH,
            task_type=self.task_type,
            created_by=self.user
        )
        response = self.client.get(
            reverse("tasks:task-list"), {"name": "Test Task 2"}
        )
        self.assertContains(response, "Test Task 2")

    def test_task_list_view_search_no_match(self):
        response = self.client.get(
            reverse("tasks:task-list"), {"name": "Nonexistent Task"}
        )
        self.assertContains(response, "There are no tasks")

    def test_task_list_view_search_empty_param(self):
        Task.objects.create(
            name="Test Task 2",
            description="Users cannot login",
            deadline=self.deadline,
            priority=Task.Priority.HIGH,
            task_type=self.task_type,
            created_by=self.user
        )
        response = self.client.get(reverse("tasks:task-list"))
        self.assertContains(response, "Test Task 2")
        self.assertContains(response, "Test Task")

    def test_task_list_view_search_invalid_param(self):
        response = self.client.get(
            reverse("tasks:task-list"),
            {"fake": "value"}
        )
        self.assertContains(response, "Test Task")


class TaskCRUDViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="user1",
            password="pass1234"
        )
        self.client.login(username="user1", password="pass1234")
        self.task_type = TaskType.objects.create(name="Bug Fix")
        self.deadline = timezone.now() + timedelta(days=7)
        self.task = Task.objects.create(
            name="Test Task",
            description="Users cannot login",
            deadline=self.deadline,
            priority=Task.Priority.HIGH,
            task_type=self.task_type,
            created_by=self.user
        )
        self.tag = Tag.objects.create(name="Test Tag")

    def test_task_create_view(self):
        response = self.client.post(
            reverse("tasks:task-create"),
            {
                "name": "New Task",
                "description": "New description",
                "deadline": self.deadline.isoformat(),
                "priority": Task.Priority.HIGH.value,
                "task_type": self.task_type.id,
                "assignees": [self.user.id],
                "tags": [self.tag.id],
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(name="New Task").exists())

    def test_task_update_view(self):
        response = self.client.post(
            reverse("tasks:task-update", kwargs={"pk": self.task.pk}),
            {
                "name": "Updated Task",
                "description": "Updated description",
                "deadline": self.deadline.isoformat(),
                "priority": Task.Priority.HIGH.value,
                "task_type": self.task_type.id,
                "assignees": [self.user.id],
                "tags": [self.tag.id],
            }
        )
        self.assertEqual(response.status_code, 302)
        self.task.refresh_from_db()
        self.assertEqual(self.task.name, "Updated Task")
        self.assertEqual(self.task.description, "Updated description")

    def test_task_delete_view(self):
        response = self.client.post(
            reverse(
                "tasks:task-delete",
                kwargs={"pk": self.task.pk}
            )
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Task.objects.filter(pk=self.task.pk).exists())


class TaskToggleViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="user1",
            password="pass1234"
        )
        self.client.login(username="user1", password="pass1234")

        self.task_type = TaskType.objects.create(name="Bug Fix")
        self.deadline = timezone.now() + timedelta(days=7)

        self.task = Task.objects.create(
            name="Test Task",
            description="Some description",
            deadline=self.deadline,
            priority=Task.Priority.HIGH,
            task_type=self.task_type,
            created_by=self.user
        )
        self.task.assignees.add(self.user)

    def test_toggle_task_by_creator_or_assignee(self):
        response = self.client.post(
            reverse(
                "tasks:task-toggle",
                args=[self.task.pk]
            )
        )
        self.task.refresh_from_db()
        self.assertTrue(self.task.is_completed)
        self.assertRedirects(response, reverse("tasks:task-list"))

    def test_toggle_task_by_non_assignee(self):
        self.other_user = User.objects.create_user(
            username="other",
            password="pass1234"
        )
        self.client.login(username="other", password="pass1234")
        response = self.client.post(
            reverse(
                "tasks:task-toggle",
                args=[self.task.pk]
            )
        )
        self.assertEqual(response.status_code, 403)


class TagViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="user1",
            password="pass1234"
        )
        self.client.login(username="user1", password="pass1234")

    def test_tag_list_view_status_code_and_template(self):
        response = self.client.get(reverse("tasks:tag-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/tag_list.html")

    def test_tag_list_view_shows_positions(self):
        Tag.objects.create(name="API")
        Tag.objects.create(name="Backend")

        response = self.client.get(reverse("tasks:tag-list"))
        self.assertContains(response, "API")
        self.assertContains(response, "Backend")

    def test_tag_list_view_empty(self):
        response = self.client.get(reverse("tasks:tag-list"))
        self.assertContains(response, "There are no Tags")

    def test_tag_list_view_search_match(self):
        Tag.objects.create(name="API")
        Tag.objects.create(name="Backend")
        response = self.client.get(
            reverse("tasks:tag-list"), {"name": "API"}
        )
        self.assertContains(response, "API")
        self.assertNotContains(response, "Backend")

    def test_tag_list_view_search_no_match(self):
        response = self.client.get(
            reverse("tasks:tag-list"), {"name": "Developer"}
        )
        self.assertNotContains(response, "Designer")

    def test_tag_list_view_search_empty_param(self):
        Tag.objects.create(name="API")
        Tag.objects.create(name="Backend")
        response = self.client.get(reverse("tasks:tag-list"))
        self.assertContains(response, "API")
        self.assertContains(response, "Backend")

    def test_tag_list_view_search_invalid_param(self):
        Tag.objects.create(name="API")
        response = self.client.get(
            reverse("tasks:tag-list"),
            {"fake": "value"}
        )
        self.assertContains(response, "API")


class TagCRUDViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="user1",
            password="pass1234"
        )
        self.client.login(username="user1", password="pass1234")
        self.tag = Tag.objects.create(name="Backend")

    def test_tag_create_view(self):
        response = self.client.post(
            reverse("tasks:tag-create"),
            {"name": "Urgent"}
        )
        self.assertRedirects(response, reverse("tasks:tag-list"))
        self.assertTrue(Tag.objects.filter(name="Urgent").exists())

    def test_tag_update_view(self):
        response = self.client.post(
            reverse(
                "tasks:tag-update",
                args=[self.tag.id]
            ),
            {"name": "Updated"})

        self.assertRedirects(response, reverse("tasks:tag-list"))
        self.tag.refresh_from_db()
        self.assertEqual(self.tag.name, "Updated")

    def test_tag_delete_view(self):
        response = self.client.post(
            reverse(
                "tasks:tag-delete",
                args=[self.tag.id]
            )
        )
        self.assertRedirects(response, reverse("tasks:tag-list"))
        self.assertFalse(Tag.objects.filter(id=self.tag.id).exists())
