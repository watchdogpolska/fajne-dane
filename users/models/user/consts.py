from django.db import models
from django.utils.translation import gettext_lazy as _


class ActionTypes(models.TextChoices):
    REGISTRATION = 'CREATED', _('Registration')
    RESETTING_PASSWORD = 'RESET_PASSWORD', _('Resetting password')
