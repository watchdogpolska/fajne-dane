from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from fajne_dane.settings import EMAIL_EXPIRATION_HOURS
from lib.utils.tokens import generate_uuid_token
from users.exceptions import ActivationTokenUsed, UserAlreadyActive, ActivationTokenExpired
from users.models.user import User


class ActionTypes(models.TextChoices):
    REGISTRATION = 'CREATED', _('Registration')
    RESETTING_PASSWORD = 'RESET_PASSWORD', _('Resetting password')


class AccountTypes(models.TextChoices):
    STANDARD = 'STANDARD', _('Standard')
    STAFF = 'STAFF', _('Staff')


class ActivationToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=32)
    created = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)
    action_type = models.CharField(max_length=20,
                                   choices=ActionTypes.choices)
    account_type = models.CharField(max_length=20,
                                    choices=AccountTypes.choices)

    @property
    def is_expired(self):
        expiration_time = self.created + timezone.timedelta(hours=EMAIL_EXPIRATION_HOURS)
        return timezone.now() > expiration_time

    def activate(self):
        if self.is_used:
            raise ActivationTokenUsed()
        if self.is_expired:
            raise ActivationTokenExpired()
        if self.user.is_active:
            raise UserAlreadyActive()

        self.user.is_active = True
        self.user.save()
        self.is_used = True
        self.save()

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = generate_uuid_token()
        super().save(*args, **kwargs)
