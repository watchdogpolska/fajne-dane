from django.db import models
from django.utils.translation import gettext_lazy as _


class InstitutionTypes(models.TextChoices):
    ORGANIZATION = 'ORGANIZATION', _('Organization')
    PERSON = 'PERSON', _('Person')
    WEBSITE = 'WEBSITE', _('Website')
    OTHER = 'OTHER', _('Other')


class InstitutionGroup(models.Model):
    """
    """
    name = models.CharField(max_length=64)
    type = models.CharField(max_length=12,
                            default=None,
                            null=False,
                            choices=InstitutionTypes.choices)
