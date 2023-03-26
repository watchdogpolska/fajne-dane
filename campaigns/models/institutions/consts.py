from typing import List

from django.db import models
from django.utils.translation import gettext_lazy as _


class InstitutionFields(models.TextChoices):
    LINK = 'link', _('Link')
    ADDRESS = 'address', _('Address')


DEFAULT_FIELDS = [
    InstitutionFields.LINK
]

def get_default_institution_fields() -> List[str]:
    return DEFAULT_FIELDS
