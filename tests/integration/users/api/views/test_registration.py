from typing import Dict

from django.test import Client, TestCase
from django.utils import timezone

from fajne_dane.settings import EMAIL_EXPIRATION_HOURS
from tests.conftest import user1
from tests.integration.users.conftest import registration_payload
from users.models import ActivationToken, User
from users.models.user.consts import ActionTypes


def activation_payload(token: str) -> Dict:
    return {
        "token": token
    }


def registration_token(user: User, is_used: bool = False) -> ActivationToken:
    token = user.create_activation_token(action_type=ActionTypes.REGISTRATION)
    if is_used:
        token.is_used = True
        token.save()
    return token


def expired_registration_token(user: User, is_used: bool = False) -> ActivationToken:
    token = registration_token(user, is_used)
    token.created -= 10 * timezone.timedelta(hours=EMAIL_EXPIRATION_HOURS)
    token.save()
    return token


class UserRegistrationTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_post(self):
        payload = registration_payload()
        response = self.client.post('/api/v1/users/register/', payload)

        self.assertEqual(response.status_code, 201)

        expected = {
            'email': 'test@email.com',
            'first_name': 'User',
            'last_name': 'Test'
        }
        self.assertEqual(response.data, expected)


class AccountActivationTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_post(self):
        user = user1()
        token = registration_token(user)
        payload = activation_payload(token=token.token)

        self.assertFalse(user.is_active)
        response = self.client.post('/api/v1/users/activate/', payload)

        user.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(user.is_active)

    def test_post_old_token(self):
        user = user1()
        old_token = registration_token(user)
        token = registration_token(user)
        old_token.refresh_from_db()
        payload = activation_payload(token=token.token)

        self.assertTrue(old_token.is_used)
        self.assertFalse(token.is_used)
        self.assertFalse(user.is_active)

        response = self.client.post('/api/v1/users/activate/', payload)
        token.refresh_from_db()

        self.assertTrue(token.is_used)

    def test_post_already_active(self):
        user = user1(is_active=True)
        token = registration_token(user)
        payload = activation_payload(token=token.token)

        response = self.client.post('/api/v1/users/activate/', payload)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['detail'], "User is already active")

    def test_post_token_already_used(self):
        user = user1(is_active=True)
        token = registration_token(user, is_used=True)
        payload = activation_payload(token=token.token)

        response = self.client.post('/api/v1/users/activate/', payload)

        self.assertEqual(response.status_code, 400)
        self.assertTrue("already used" in str(response.data['detail']))

    def test_post_token_expired(self):
        user = user1()
        token = expired_registration_token(user)
        payload = activation_payload(token=token.token)

        response = self.client.post('/api/v1/users/activate/', payload)

        self.assertEqual(response.status_code, 400)
        self.assertTrue("expired" in str(response.data['detail']))
