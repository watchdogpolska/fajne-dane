from typing import Text

from django.db import models

from campaigns.models.institutions.instituion_group import InstitutionTypes


class Institution(models.Model):
    """
    """
    group = models.ForeignKey("InstitutionGroup",
                             on_delete=models.CASCADE,
                             related_name="institutions")
    key = models.CharField(max_length=64, unique=True)
    name = models.CharField(max_length=64)
    link = models.CharField(max_length=64)
    address = models.CharField(max_length=64)

    @property
    def type(self) -> Text:
        return self.group.type
