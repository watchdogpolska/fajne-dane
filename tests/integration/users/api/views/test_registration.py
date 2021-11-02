from typing import Dict
from unittest.mock import patch

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


def registration_payload_missing_fields() -> Dict:
    return {
        'email': 'test@email.com',
        'first_name': 'User',
        'last_name': 'Test'
    }


def user_email_payload(user) -> Dict:
    return {
        'email': user.email
    }


def expired_registration_token(user: User, is_used: bool = False) -> ActivationToken:
    token = registration_token(user, is_used)
    token.created -= 10 * timezone.timedelta(hours=EMAIL_EXPIRATION_HOURS)
    token.save()
    return token


class UserRegistrationTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    @patch('fajne_dane.lib.emails.helper.send_registration_email')
    def test_post(self, mocked_sending):
        payload = registration_payload()
        response = self.client.post('/api/v1/users/register/', payload)

        # check if the response was correct
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.data,
            {
                'email': 'test@email.com',
                'first_name': 'User',
                'last_name': 'Test'
            }
        )

        # check if email was sent
        user = User.objects.get(email="test@email.com")
        self.assertIsInstance(user, User)
        mocked_sending.assert_called_with(user, user.get_activation_token(ActionTypes.REGISTRATION))

    def test_post_invalid_payload(self):
        response = self.client.post('/api/v1/users/register/', registration_payload_missing_fields())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(list(response.data.keys()), ['password', 'password_confirmation'])


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
        self.assertEqual(response.status_code, 204)
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

        self.client.post('/api/v1/users/activate/', payload)
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


class TokenReactivationTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    @patch('fajne_dane.lib.emails.helper.send_registration_email')
    def test_post(self, mocked_sending):
        user = user1()

        response = self.client.post('/api/v1/users/activate/resend/', user_email_payload(user))
        self.assertEqual(response.status_code, 204)

        mocked_sending.assert_called_with(user, user.get_activation_token(ActionTypes.REGISTRATION))

    def test_post_not_existing_user(self):
        payload = {
            "email": "other@email.com"
        }

        response = self.client.post('/api/v1/users/activate/resend/', payload)
        self.assertEqual(response.status_code, 400)
        self.assertTrue("email not found" in str(response.data['detail']))
