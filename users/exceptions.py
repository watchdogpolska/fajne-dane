from rest_framework import status
from rest_framework.exceptions import APIException


class AccountInactive(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = 'Account is not active'
    default_code = 'account_not_active'


class EmailUsed(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Email is already used'
    default_code = 'email_used'


class PasswordsNotMatch(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Passwords does not match'
    default_code = 'passwords_not_match'


class PasswordIncorrect(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Password was incorrect'
    default_code = 'password_incorrect'


class UnableToAuthenticate(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Unable to authenticate'
    default_code = 'authentication_error'


class ActivationTokenWrong(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Activation token is incorrect'
    default_code = 'activation_token_wrong'


class ActivationTokenExpired(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Activation token has expired'
    default_code = 'activation_token_expired'


class ActivationTokenUsed(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Activation token is already used'
    default_code = 'activation_token_used'


class EmailNotFound(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'User with following email not found'
    default_code = 'email_not_found'


class UserAlreadyActive(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'User is already active'
    default_code = 'user_active'
