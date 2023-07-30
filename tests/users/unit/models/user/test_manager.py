from django.test import TestCase

from tests.conftest import user1
from users.models import User, ActivationToken
from users.models.user.consts import ActionTypes


class CreatingUserTestCase(TestCase):

    def test_creating(self):
        user = User.objects.create_user(
            email="test@email.com", password="testpass",
            first_name="Test", last_name="User")
        self.assertIsInstance(user, User)
        self.assertEqual(user.email, "test@email.com")
        self.assertEqual(user.first_name, "Test")
        self.assertEqual(user.last_name, "User")

    def test_creating_without_password(self):
        user = User.objects.create_user(email="test@email.com")
        self.assertIsInstance(user, User)
        self.assertEqual(user.email, "test@email.com")

    def test_creating_without_email(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(email=None, password="test_pass")

    def test_creating_superuser(self):
        user = User.objects.create_superuser(
            email="test@email.com", password="testpass",
            first_name="Test", last_name="User")
        self.assertIsInstance(user, User)
        self.assertEqual(user.email, "test@email.com")
        self.assertEqual(user.first_name, "Test")
        self.assertEqual(user.last_name, "User")
        self.assertEqual(user.is_superuser, True)
        self.assertEqual(user.is_staff, True)

    def test_creating_superuser_no_superuser(self):
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email="test@email.com", password="Pass", is_superuser=False)

    def test_creating_superuser_no_staff(self):
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email="test@email.com", password="Pass", is_staff=False)
