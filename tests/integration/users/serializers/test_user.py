from django.test import TestCase

from tests.conftest import user1
from tests.integration.users.conftest import (
    registration_payload,
    registration_payload_passwords_not_match,
    registration_payload_used_email
)
from users.exceptions import PasswordsNotMatch, EmailUsed
from users.models import User
from users.serializers.user import UserRegistrationSerializer


class UserSerializerTestCase(TestCase):
    ...


class UserRegistrationSerializerTestCase(TestCase):
    def test_create(self):
        payload = registration_payload()
        serializer = UserRegistrationSerializer(data=payload)
        serializer.is_valid()
        serializer.save()

        user = User.objects.get(email=payload['email'])
        self.assertIsInstance(user, User)

    def test_validate_passwords(self):
        payload = registration_payload_passwords_not_match()
        serializer = UserRegistrationSerializer(data=payload)

        with self.assertRaises(PasswordsNotMatch):
            serializer.is_valid()

    def test_validate_email(self):
        user1()  # add first user
        payload = registration_payload_used_email()

        serializer = UserRegistrationSerializer(data=payload)
        with self.assertRaises(EmailUsed):
            serializer.is_valid()
