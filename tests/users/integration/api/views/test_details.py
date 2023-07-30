import json
from typing import Dict

from django.test import Client, TestCase

from tests.conftest import user1


class DetailsTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_get_details(self):
        user = user1(is_active=True)
        self.client.force_login(user)
        response = self.client.get('/api/v1/users/details/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data,
            {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email
            }
        )

    def test_get_details_not_logged(self):
        user1(is_active=True)
        response = self.client.get('/api/v1/users/details/')
        self.assertEqual(response.status_code, 401)


class UpdateDetailsTestCase(TestCase):
    def test_put_details(self):
        user = user1(is_active=True)
        self.client.force_login(user)
        payload = {
            'first_name': user.first_name,
            'last_name': user.last_name,
        }
        response = self.client.put(
            f'/api/v1/users/details/',
            data=json.dumps(payload),
            content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_put_details_not_logged(self):
        user1(is_active=True)
        response = self.client.put('/api/v1/users/details/', {})
        self.assertEqual(response.status_code, 401)
