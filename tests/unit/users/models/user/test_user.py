from unittest.mock import patch

from django.test import TestCase
from rest_framework.authtoken.models import Token

from tests.conftest import user1
from users.exceptions import UserAlreadyActive
from users.models import User, ActivationToken
from users.models.user.consts import ActionTypes


def user_with_tokens() -> User:
    user = user1()
    user.create_activation_token(action_type=ActionTypes.REGISTRATION)
    user.create_activation_token(action_type=ActionTypes.RESETTING_PASSWORD)
    return user


def user_with_multiple_tokens() -> User:
    user = user1()
    user.create_activation_token(action_type=ActionTypes.RESETTING_PASSWORD)
    user.create_activation_token(action_type=ActionTypes.RESETTING_PASSWORD)
    user.create_activation_token(action_type=ActionTypes.RESETTING_PASSWORD)
    return user


class CreatingTokensTestCase(TestCase):

    def test_creating_registration_token(self):
        user = user1()
        token = user.create_activation_token(action_type=ActionTypes.REGISTRATION)
        self.assertIsInstance(token, ActivationToken)
        self.assertEqual(token.user, user)
        self.assertEqual(token.action_type, ActionTypes.REGISTRATION)

    def test_creating_password_token(self):
        user = user1()
        token = user.create_activation_token(action_type=ActionTypes.RESETTING_PASSWORD)
        self.assertIsInstance(token, ActivationToken)
        self.assertEqual(token.user, user)
        self.assertEqual(token.action_type, ActionTypes.RESETTING_PASSWORD)

    def test_getting_token(self):
        user = user_with_tokens()
        token = user.get_activation_token(action_type=ActionTypes.REGISTRATION)
        self.assertIsInstance(token, ActivationToken)
        self.assertEqual(token.action_type, ActionTypes.REGISTRATION)

    def test_getting_token_multiple(self):
        user = user_with_multiple_tokens()
        token = user.get_activation_token(action_type=ActionTypes.RESETTING_PASSWORD)
        self.assertIsInstance(token, ActivationToken)

    def test_creating_token_closing_existing(self):
        user = user_with_tokens()
        password_token = user.get_activation_token(action_type=ActionTypes.RESETTING_PASSWORD)
        registration_token = user.get_activation_token(action_type=ActionTypes.REGISTRATION)
        self.assertFalse(password_token.is_used)
        self.assertFalse(registration_token.is_used)

        user.create_activation_token(action_type=ActionTypes.REGISTRATION)
        registration_token = ActivationToken.objects.get(token=registration_token.token)
        self.assertFalse(password_token.is_used)
        self.assertTrue(registration_token.is_used)


class SendingTokenEmailsTestCase(TestCase):
    @patch('lib.emails.helper.send_registration_email')
    def test_sending_registration_email(self, mocked_sending):
        user = user1()
        user.send_registration_email()
        mocked_sending.assert_called_with(user, user.get_activation_token(ActionTypes.REGISTRATION))

    def test_sending_registration_email_already_active(self):
        user = user1(is_active=True)
        with self.assertRaises(UserAlreadyActive):
            user.send_registration_email()

    @patch('lib.emails.helper.send_reset_password_email')
    def test_sending_reset_password_email(self, mocked_sending):
        user = user1()
        user.send_reset_password_email()
        mocked_sending.assert_called_with(user, user.get_activation_token(ActionTypes.RESETTING_PASSWORD))


class CreatingTokenTestCase(TestCase):
    def test_get_token(self):
        user = user1()
        token = user.token
        self.assertIsInstance(token, Token)

    def test_reusing_token(self):
        user = user1()
        token = user.token
        self.assertEqual(token, user.token)
