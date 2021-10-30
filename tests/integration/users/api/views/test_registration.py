from typing import Dict

from django.test import Client, TestCase

from tests.conftest import user1
from tests.integration.users.conftest import registration_payload
from users.models import ActivationToken, User
from users.models.user.consts import ActionTypes


def activation_payload(token: str) -> Dict:
    return {
        "token": token
    }


def registration_token(user: User) -> ActivationToken:
    return user.create_activation_token(action_type=ActionTypes.REGISTRATION)


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

        user = User.objects.get(id=user.id)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(user.is_active)
