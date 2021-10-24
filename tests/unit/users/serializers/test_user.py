from typing import Dict

from django.test import TestCase

from users.exceptions import PasswordsNotMatch
from users.models import User
from users.serializers.user import UserRegistrationSerializer


def registration_payload() -> Dict:
    return {
        "username": "testuser",
        "email": "test@email.com",
        "first_name": "User",
        "last_name": "Test",
        "password1": "testpass123",
        "password2": "testpass123",
    }

def registration_payload_passwords_not_match() -> Dict:
    payload = registration_payload()
    payload['password2'] = "otherpassword"
    return payload


class UserSerializerTestCase(TestCase):
    ...


class UserRegistrationSerializerTestCase(TestCase):
    def test_create(self):
        payload = registration_payload()
        serializer = UserRegistrationSerializer(data=payload)
        serializer.is_valid()
        serializer.save()

        user = User.objects.get(username=payload['username'])
        self.assertIsInstance(user, User)

    def test_validate_passwords(self):
        payload = registration_payload_passwords_not_match()
        serializer = UserRegistrationSerializer(data=payload)

        with self.assertRaises(PasswordsNotMatch):
            serializer.is_valid()
