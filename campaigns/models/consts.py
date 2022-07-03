from django.db import models
from django.utils.translation import gettext_lazy as _


class CampaignStatus(models.TextChoices):
    CREATED = 'CREATED', _('Created')
    INITIALIZED = 'INITIALIZED', _('Initialized')
    VALIDATING = 'VALIDATING', _('Validating')
    CLOSED = 'CLOSED', _('Closed')


class DocumentStatus(models.TextChoices):
    CREATED = 'CREATED', _('Created')
    INITIALIZED = 'INITIALIZED', _('Initialized')
    VALIDATING = 'VALIDATING', _('Validating')
    CLOSED = 'CLOSED', _('Closed')


class DocumentQueryStatus(models.TextChoices):
    CREATED = 'CREATED', _('Created')
    INITIALIZED = 'INITIALIZED', _('Initialized')
    CLOSED = 'CLOSED', _('Closed')


class RecordStatus(models.TextChoices):
    NONE = 'NONE', _('None')
    ACCEPTED = 'ACCEPTED', _('Accepted')
    REJECTED = 'REJECTED', _('Rejected')


class CampaignStatus(models.TextChoices):
    CREATED = 'CREATED', _('Created')
    INITIALIZED = 'INITIALIZED', _('Initialized')
    VALIDATING = 'VALIDATING', _('Validating')
    CLOSED = 'CLOSED', _('Closed')
