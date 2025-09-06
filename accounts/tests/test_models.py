from django.test import TestCase

from accounts.models import Position, Worker


class PositionModelTests(TestCase):
    def test_position_creation_and_str(self):
        position = Position.objects.create(name="Developer")
        self.assertEqual(str(position), "Developer")


class WorkerModelTests(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="Developer")

    def test_worker_creation_and_str(self):
        user = Worker.objects.create_user(
            username="john",
            password="Testpass123",
            position=self.position
        )
        self.assertEqual(str(user), "john")
        self.assertEqual(user.position, self.position)
