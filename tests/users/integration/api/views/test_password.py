import json
from tests.conftest import user1
from users.models.user import ActionTypes
from django.test import Client, TestCase


class PasswordTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_rest(self):
        user = user1(is_active=True)
        self.client.force_login(user)

        token = user.create_activation_token(ActionTypes.RESETTING_PASSWORD)

        payload = {
            'token': token.token,
            'password': 'password',
            'password_confirmation': 'password'
        }
        response = self.client.post(
            '/api/v1/users/password/reset/',
            data=json.dumps(payload),
            content_type='application/json')
        self.assertEqual(response.status_code, 204)
