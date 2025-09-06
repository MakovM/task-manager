from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from tasks.models import Tag, TaskType, Task

Worker = get_user_model()


class TaskModelTests(TestCase):
    def setUp(self):
        self.user = Worker.objects.create_user(
            username="testuser",
            password="Testpass123"
        )
        self.task_type  =TaskType.objects.create(name="Bug Fix")
        self.deadline = timezone.now() + timedelta(days=7)


    def test_task_creation_and_string_representation(self):
        task = Task.objects.create(
            name="Fix login bug",
            description="Users cannot login",
            deadline=self.deadline,
            priority=Task.Priority.HIGH,
            task_type=self.task_type,
            created_by=self.user,
        )
        self.assertEqual(str(task), "Fix login bug")

    def test_task_default_values(self):
        task = Task.objects.create(
            name="Test task",
            description="Some description",
            deadline=self.deadline,
            task_type=self.task_type,
            created_by=self.user,
        )
        self.assertFalse(task.is_completed)
        self.assertEqual(task.priority, Task.Priority.MEDIUM)

    def test_task_assignees_relationship(self):
        assignee = Worker.objects.create_user(
            username="assignee", password="testpass123"
        )
        task = Task.objects.create(
            name="Test task",
            description="Some description",
            deadline=self.deadline,
            task_type=self.task_type,
            created_by=self.user,
        )
        task.assignees.add(assignee)

        self.assertIn(assignee, task.assignees.all())
        self.assertIn(task, assignee.assigned_tasks.all())

    def test_task_tags_relationship(self):
        tag1 = Tag.objects.create(name="Backend")
        tag2 = Tag.objects.create(name="Urgent")
        task = Task.objects.create(
            name="Test task",
            description="Some description",
            deadline=self.deadline,
            task_type=self.task_type,
            created_by=self.user,
        )
        task.tags.add(tag1, tag2)

        self.assertIn(tag1, task.tags.all())
        self.assertIn(tag2, task.tags.all())
        self.assertIn(task, tag1.tasks.all())

class TaskTypeModelTests(TestCase):
    def test_task_type_creation_and_str(self):
        task_type = TaskType.objects.create(name="Feature")
        self.assertEqual(str(task_type), "Feature")


class TagModelTests(TestCase):
    def test_tag_creation_and_str(self):
        tag = Tag.objects.create(name="Backend")
        self.assertEqual(str(tag), "Backend")
