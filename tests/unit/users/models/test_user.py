from django.test import TestCase

from tests.conftest import user1
from users.models import User, ActivationToken
from users.models.user.consts import ActionTypes


def user_with_tokens() -> User:
    user = user1()
    user.create_activation_token(action_type=ActionTypes.REGISTRATION)
    user.create_activation_token(action_type=ActionTypes.RESETTING_PASSWORD)
    return user


def user_with_multiple_tokens() -> User:
    user = user1()
    user.create_activation_token(action_type=ActionTypes.RESETTING_PASSWORD)
    user.create_activation_token(action_type=ActionTypes.RESETTING_PASSWORD)
    user.create_activation_token(action_type=ActionTypes.RESETTING_PASSWORD)
    return user



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


class CreatingTokensTestCase(TestCase):

    def test_creating_registration_token(self):
        user = user1()
        token = user.create_activation_token(action_type=ActionTypes.REGISTRATION)
        self.assertIsInstance(token, ActivationToken)
        self.assertEqual(token.user, user)
        self.assertEqual(token.action_type, ActionTypes.REGISTRATION)

    def test_creating_password_token(self):
        user = user1()
        token = user.create_activation_token(action_type=ActionTypes.RESETTING_PASSWORD)
        self.assertIsInstance(token, ActivationToken)
        self.assertEqual(token.user, user)
        self.assertEqual(token.action_type, ActionTypes.RESETTING_PASSWORD)

    def test_getting_token(self):
        user = user_with_tokens()
        token = user.get_activation_token(action_type=ActionTypes.REGISTRATION)
        self.assertIsInstance(token, ActivationToken)
        self.assertEqual(token.action_type, ActionTypes.REGISTRATION)

    def test_getting_token_multiple(self):
        user = user_with_multiple_tokens()
        token = user.get_activation_token(action_type=ActionTypes.RESETTING_PASSWORD)
        self.assertIsInstance(token, ActivationToken)

    def test_creating_token_closing_existing(self):
        user = user_with_tokens()
        password_token = user.get_activation_token(action_type=ActionTypes.RESETTING_PASSWORD)
        registration_token = user.get_activation_token(action_type=ActionTypes.REGISTRATION)
        self.assertFalse(password_token.is_used)
        self.assertFalse(registration_token.is_used)

        user.create_activation_token(action_type=ActionTypes.REGISTRATION)
        registration_token = ActivationToken.objects.get(token=registration_token.token)
        self.assertFalse(password_token.is_used)
        self.assertTrue(registration_token.is_used)
