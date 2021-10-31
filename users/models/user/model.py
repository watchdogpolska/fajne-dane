from typing import Optional

from django.apps import apps
from django.contrib.auth.models import AbstractUser
from django.db import models

from lib.emails import helper
from .consts import ActionTypes
from .manager import UserManager
from ...exceptions import UserAlreadyActive


class User(AbstractUser):
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

    def send_activation_token_email(self, action_type: ActionTypes):
        if self.is_active:
            raise UserAlreadyActive()

        token = self.create_activation_token(action_type)
        if action_type == ActionTypes.REGISTRATION:
            helper.send_registration_email(self, token)
        elif action_type == ActionTypes.RESETTING_PASSWORD:
            helper.send_reset_password_email(self, token)
