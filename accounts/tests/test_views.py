from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from accounts.models import Position


User = get_user_model()


class SignUpViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_signup_view_get(self):
        response = self.client.get(reverse("accounts:sign-up"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/signup.html")

    def test_signup_view_post_creates_user(self):
        data = {
            "username": "newuser",
            "email": "test@admin.com",
            "password1": "Testpass123",
            "password2": "Testpass123",
        }
        response = self.client.post(reverse("accounts:sign-up"), data)
        self.assertRedirects(response, reverse("accounts:login"))
        self.assertTrue(User.objects.filter(username="newuser").exists())


class WorkerListViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="user1",
            password="Testpass123"
        )
        self.client.login(username="user1", password="Testpass123")

    def test_worker_list_view_status_code_and_template(self):
        response = self.client.get(reverse("accounts:worker-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/worker_list.html")

    def test_worker_list_view_search_match(self):
        User.objects.create_user(username="user2", password="Testpass123")
        response = self.client.get(
            reverse("accounts:worker-list"), {"username": "user1"}
        )
        self.assertContains(response, "user1")
        self.assertNotContains(response, "user2")

    def test_worker_list_view_search_no_match(self):
        response = self.client.get(
            reverse("accounts:worker-list"), {"username": "user1"}
        )
        self.assertNotContains(response, "user2")

    def test_worker_list_view_search_empty_param(self):
        User.objects.create_user(username="user2", password="Testpass123")
        response = self.client.get(reverse("accounts:worker-list"))
        self.assertContains(response, "user1")
        self.assertContains(response, "user2")

    def test_worker_list_view_search_invalid_param(self):
        response = self.client.get(
            reverse("accounts:worker-list"),
            {"fake": "value"}
        )
        self.assertContains(response, "user1")


class WorkerDetailViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="user1",
            password="Testpass123"
        )
        self.client.login(username="user1", password="Testpass123")

    def test_worker_detail_view(self):
        response = self.client.get(
            reverse(
                "accounts:worker-detail",
                args=[self.user.pk]
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.username)


class WorkerUpdateDeleteViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="user1",
            password="Testpass123"
        )
        self.client.login(username="user1", password="Testpass123")

    def test_worker_update_view(self):
        response = self.client.post(
            reverse("accounts:worker-update", args=[self.user.pk]),
            {"username": "updated_user", "position": ""},
        )
        self.assertRedirects(
            response,
            reverse("accounts:worker-detail", args=[self.user.pk])
        )
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, "updated_user")

    def test_worker_delete_view(self):
        response = self.client.post(
            reverse(
                "accounts:worker-delete",
                args=[self.user.pk]
            )
        )
        self.assertRedirects(response, reverse("accounts:login"))
        self.assertFalse(User.objects.filter(pk=self.user.pk).exists())


class WorkerPasswordChangeViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="user1",
            password="Testpass123"
        )
        self.client.login(username="user1", password="Testpass123")

    def test_password_change_get(self):
        response = self.client.get(
            reverse(
                "accounts:password-change",
                args=[self.user.id]
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/change_password.html")

    def test_password_change_post_valid(self):
        response = self.client.post(
            reverse("accounts:password-change", args=[self.user.id]),
            {
                "old_password": "Testpass123",
                "new_password1": "Newpass12345",
                "new_password2": "Newpass12345",
            },
        )
        self.assertRedirects(
            response,
            reverse("accounts:worker-detail", args=[self.user.id]),
        )

        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("Newpass12345"))

    def test_password_change_post_invalid(self):
        response = self.client.post(
            reverse("accounts:password-change", args=[self.user.id]),
            {
                "old_password": "wrongpass",
                "new_password1": "Newpass12345",
                "new_password2": "Newpass12345",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("Testpass123"))


class WorkerPositionChangeViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.staff_user = User.objects.create_user(
            username="admin",
            password="Testpass123",
            is_staff=True
        )
        self.normal_user = User.objects.create_user(
            username="user1",
            password="Testpass123",
            is_staff=False
        )
        self.position = Position.objects.create(name="Developer")

    def test_staff_can_change_position_of_other_user(self):
        self.client.login(username="admin", password="Testpass123")

        response = self.client.post(
            reverse("accounts:position-change", args=[self.normal_user.id]),
            {"position": self.position.id},
        )
        self.assertRedirects(
            response,
            reverse("accounts:worker-detail", args=[self.normal_user.id]),
        )
        self.normal_user.refresh_from_db()
        self.assertEqual(self.normal_user.position, self.position)

    def test_staff_cannot_change_own_position(self):
        self.client.login(username="admin", password="Testpass123")

        response = self.client.post(
            reverse("accounts:position-change", args=[self.staff_user.id]),
            {"position": self.position.id},
        )
        self.assertEqual(response.status_code, 403)
        self.staff_user.refresh_from_db()
        self.assertIsNone(self.staff_user.position)

    def test_non_staff_cannot_change_position(self):
        self.client.login(username="user1", password="Testpass123")

        response = self.client.post(
            reverse("accounts:position-change", args=[self.normal_user.id]),
            {"position": self.position.id},
        )
        self.assertEqual(response.status_code, 403)
        self.normal_user.refresh_from_db()
        self.assertIsNone(self.normal_user.position)


class WorkerStatusChangeViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.staff_user = User.objects.create_user(
            username="admin", password="Testpass123", is_staff=True
        )
        self.normal_user = User.objects.create_user(
            username="user1", password="Testpass123", is_staff=False
        )

    def test_staff_can_toggle_status(self):
        self.client.login(username="admin", password="Testpass123")
        self.assertFalse(self.normal_user.is_staff)

        response = self.client.post(
            reverse("accounts:status-change", args=[self.normal_user.id])
        )
        self.assertRedirects(
            response,
            reverse("accounts:worker-detail", args=[self.normal_user.id])
        )
        self.normal_user.refresh_from_db()
        self.assertTrue(self.normal_user.is_staff)

    def test_non_staff_cannot_toggle_status(self):
        self.client.login(username="user1", password="Testpass123")
        response = self.client.post(
            reverse("accounts:status-change", args=[self.normal_user.id])
        )
        self.assertEqual(response.status_code, 403)
        self.normal_user.refresh_from_db()
        self.assertFalse(self.normal_user.is_staff)


class PositionListViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="user1",
            password="Testpass123"
        )
        self.client.login(username="user1", password="Testpass123")

    def test_position_list_view_status_code_and_template(self):
        response = self.client.get(reverse("accounts:position-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/position_list.html")

    def test_position_list_view_shows_positions(self):
        Position.objects.create(name="Developer")
        Position.objects.create(name="Manager")

        response = self.client.get(reverse("accounts:position-list"))
        self.assertContains(response, "Developer")
        self.assertContains(response, "Manager")

    def test_position_list_view_empty(self):
        response = self.client.get(reverse("accounts:position-list"))
        self.assertContains(response, "There are no Positions")

    def test_position_list_view_search_match(self):
        Position.objects.create(name="Developer")
        Position.objects.create(name="Designer")
        response = self.client.get(
            reverse("accounts:position-list"), {"name": "Designer"}
        )
        self.assertContains(response, "Designer")
        self.assertNotContains(response, "Developer")

    def test_position_list_view_search_no_match(self):
        response = self.client.get(
            reverse("accounts:position-list"), {"name": "Developer"}
        )
        self.assertNotContains(response, "Designer")

    def test_position_list_view_search_empty_param(self):
        Position.objects.create(name="Developer")
        Position.objects.create(name="Designer")
        response = self.client.get(reverse("accounts:position-list"))
        self.assertContains(response, "Developer")
        self.assertContains(response, "Designer")

    def test_position_list_view_search_invalid_param(self):
        Position.objects.create(name="Developer")
        response = self.client.get(
            reverse("accounts:position-list"),
            {"fake": "value"}
        )
        self.assertContains(response, "Developer")


class PositionCRUDViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="user1",
            password="Testpass123"
        )
        self.client.login(username="user1", password="Testpass123")
        self.position = Position.objects.create(name="Developer")

    def test_position_create_view(self):
        response = self.client.post(
            reverse("accounts:position-create"),
            {"name": "Manager"},
        )
        self.assertRedirects(response, reverse("accounts:position-list"))
        self.assertTrue(Position.objects.filter(name="Manager").exists())

    def test_position_update_view(self):
        response = self.client.post(
            reverse("accounts:position-update", args=[self.position.pk]),
            {"name": "Senior Developer"},
        )
        self.assertRedirects(response, reverse("accounts:position-list"))
        self.position.refresh_from_db()
        self.assertEqual(self.position.name, "Senior Developer")

    def test_position_delete_view(self):
        response = self.client.post(
            reverse("accounts:position-delete", args=[self.position.pk])
        )
        self.assertRedirects(response, reverse("accounts:position-list"))
        self.assertFalse(Position.objects.filter(pk=self.position.pk).exists())
