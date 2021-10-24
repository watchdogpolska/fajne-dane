from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from fajne_dane.settings import EMAIL_EXPIRATION_HOURS
from tests.conftest import user1
from users.exceptions import ActivationTokenExpired, ActivationTokenUsed, UserAlreadyActive
from users.models.activation_token import ActivationToken, ActionTypes, AccountTypes


def activation_token() -> ActivationToken:
    return ActivationToken.objects.create(
        user=user1(),
        action_type=ActionTypes.REGISTRATION,
        account_type=AccountTypes.STANDARD
    )


def expired_activation_token() -> ActivationToken:
    token = activation_token()
    token.created -= 10 * timezone.timedelta(hours=EMAIL_EXPIRATION_HOURS)
    token.save()
    return token


class ActivationTokenTestCase(TestCase):

    def test_creating_token(self):
        token = ActivationToken.objects.create(
            user=user1(),
            action_type=ActionTypes.REGISTRATION,
            account_type=AccountTypes.STANDARD
        )
        self.assertIsInstance(token, ActivationToken)
        self.assertTrue(len(token.token) > 0)

    def test_not_expired_token(self):
        token = activation_token()
        self.assertFalse(token.is_expired)

    def test_expired_token(self):
        token = expired_activation_token()
        self.assertTrue(token.is_expired)

    def test_activate(self):
        token = activation_token()

        self.assertFalse(token.user.is_active)
        token.activate()
        self.assertTrue(token.user.is_active)
        self.assertTrue(token.is_used)

    def test_activate_expired_token(self):
        token = expired_activation_token()
        with self.assertRaises(ActivationTokenExpired):
            token.activate()

    def test_activate_user_token(self):
        token = activation_token()
        token.activate()
        with self.assertRaises(ActivationTokenUsed):
            token.activate()

    def test_activate_user_token(self):
        user1(is_active=True)
        token = activation_token()
        with self.assertRaises(UserAlreadyActive):
            token.activate()
