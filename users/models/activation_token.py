from django.db import models
from django.utils import timezone

from fajne_dane.settings import EMAIL_EXPIRATION_HOURS
from fajne_dane.core.utils import generate_uuid_token
from users.exceptions import ActivationTokenUsed, UserAlreadyActive, ActivationTokenExpired, WrongTokenType
from users.models.user import ActionTypes, User


class ActivationToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=32)
    created = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)
    action_type = models.CharField(max_length=20,
                                   choices=ActionTypes.choices)

    @property
    def is_expired(self):
        expiration_time = self.created + timezone.timedelta(hours=EMAIL_EXPIRATION_HOURS)
        return timezone.now() > expiration_time

    def activate(self):
        if self.action_type != ActionTypes.REGISTRATION:
            raise WrongTokenType()

        self.use()

        if self.user.is_active:
            raise UserAlreadyActive()

        self.user.is_active = True
        self.user.save()

    def use(self):
        if self.is_used:
            raise ActivationTokenUsed()
        if self.is_expired:
            raise ActivationTokenExpired()
        self.is_used = True
        self.save()

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = generate_uuid_token()
        super().save(*args, **kwargs)
