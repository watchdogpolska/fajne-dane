from typing import Optional

from django.apps import apps
from django.contrib.auth.models import AbstractUser
from django.db import models

from fajne_dane.core.emails import helper as email_helper
from .consts import ActionTypes
from .manager import UserManager
from ...exceptions import UserAlreadyActive


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

    def _close_activation_tokens(self, action_type: ActionTypes):
        ActivationToken = apps.get_model("users.ActivationToken")
        tokens = []
        for token in ActivationToken.objects.filter(user=self, action_type=action_type):
            token.is_used = True
            tokens.append(token)
        if tokens:
            ActivationToken.objects.bulk_update(tokens, fields=['is_used'])

    def create_activation_token(self, action_type: ActionTypes) -> "ActivationToken":
        self._close_activation_tokens(action_type=action_type)

        ActivationToken = apps.get_model("users.ActivationToken")
        return ActivationToken.objects.create(user=self, action_type=action_type)

    def get_activation_token(self, action_type: ActionTypes) -> Optional["ActivationToken"]:
        ActivationToken = apps.get_model("users.ActivationToken")
        return ActivationToken.objects.filter(user=self, action_type=action_type).last()

    def send_registration_email(self):
        if self.is_active:
            raise UserAlreadyActive()
        token = self.create_activation_token(ActionTypes.REGISTRATION)
        email_helper.send_registration_email(self, token)

    def send_reset_password_email(self):
        token = self.create_activation_token(ActionTypes.RESETTING_PASSWORD)
        email_helper.send_reset_password_email(self, token)
