from django.test import TestCase
from django.utils import timezone

from fajne_dane.settings import EMAIL_EXPIRATION_HOURS
from tests.conftest import user1
from users.exceptions import ActivationTokenExpired, ActivationTokenUsed, UserAlreadyActive
from users.models import User
from users.models.activation_token import ActivationToken, ActionTypes


def activation_token(user: User) -> ActivationToken:
    return ActivationToken.objects.create(
        user=user,
        action_type=ActionTypes.REGISTRATION
    )


def expired_activation_token(user: User) -> ActivationToken:
    token = activation_token(user)
    token.created -= 10 * timezone.timedelta(hours=EMAIL_EXPIRATION_HOURS)
    token.save()
    return token


class ActivationTokenTestCase(TestCase):

    def test_creating_token(self):
        token = ActivationToken.objects.create(
            user=user1(),
            action_type=ActionTypes.REGISTRATION
        )
        self.assertIsInstance(token, ActivationToken)
        self.assertTrue(len(token.token) > 0)

    def test_not_expired_token(self):
        token = activation_token(user1())
        self.assertFalse(token.is_expired)

    def test_expired_token(self):
        token = expired_activation_token(user1())
        self.assertTrue(token.is_expired)

    def test_activate(self):
        token = activation_token(user1())

        self.assertFalse(token.user.is_active)
        token.activate()
        self.assertTrue(token.user.is_active)
        self.assertTrue(token.is_used)

    def test_activate_expired_token(self):
        token = expired_activation_token(user1())
        with self.assertRaises(ActivationTokenExpired):
            token.activate()

    def test_activate_user_token(self):
        token = activation_token(user1())
        token.activate()
        with self.assertRaises(ActivationTokenUsed):
            token.activate()

    def test_activate_user_token(self):
        token = activation_token(user1(is_active=True))
        with self.assertRaises(UserAlreadyActive):
            token.activate()
