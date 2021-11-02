from typing import Dict

from django.test import Client, TestCase

from tests.conftest import user1


def user_login_payload(email: str, password: str = "password") -> Dict:
    return {
        "email": email,
        "password": password
    }


class LoginTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_login(self):
        user = user1(is_active=True)
        payload = user_login_payload(user.email)
        response = self.client.post('/api/v1/users/login/', payload)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data,
            {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'token': str(user.token)
            }
        )

    def test_login_inactive_user(self):
        user = user1(is_active=False)
        payload = user_login_payload(user.email)
        response = self.client.post('/api/v1/users/login/', payload)

        self.assertEqual(response.status_code, 400)
        self.assertEqual("Unable to authenticate", str(response.data['detail']))



    def test_login_user_not_found(self):
        payload = user_login_payload("test@mail.com", "password")
        response = self.client.post('/api/v1/users/login/', payload)

        self.assertEqual(response.status_code, 400)
        self.assertEqual("Unable to authenticate", str(response.data['detail']))

    def test_login_wrong_password(self):
        user = user1(is_active=True)
        payload = user_login_payload(user.email, "wrong_pass")
        response = self.client.post('/api/v1/users/login/', payload)

        self.assertEqual(response.status_code, 400)
        self.assertEqual("Unable to authenticate", str(response.data['detail']))


class LogoutTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_logout(self):
        user = user1(is_active=True)
        self.client.force_login(user)

        # check if logged in
        response = self.client.get(f'/api/v1/users/{user.id}/')
        self.assertEqual(response.status_code, 200)

        # logout
        response = self.client.get(f'/api/v1/users/logout/')
        self.assertEqual(response.status_code, 204)

        # check if logged in
        response = self.client.get(f'/api/v1/users/{user.id}/')
        self.assertEqual(response.status_code, 401)


    def test_logout_not_authenticated(self):
        response = self.client.get(f'/api/v1/users/logout/')
        self.assertEqual(response.status_code, 401)


class AuthenticationTokenTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_token_auth(self):
        user = user1(is_active=True)
        response = self.client.get(f'/api/v1/users/{user.id}/',
                                   HTTP_AUTHORIZATION='Token {}'.format(user.token))
        self.assertEqual(response.status_code, 200)
