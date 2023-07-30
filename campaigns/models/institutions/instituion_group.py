from django.db import models
from django.contrib.postgres.fields import ArrayField

from campaigns.models.institutions.consts import InstitutionFields, get_default_institution_fields


class InstitutionGroup(models.Model):
    """
    """
    name = models.CharField(max_length=64)
    fields = ArrayField(models.CharField(max_length=32,
                                         choices=InstitutionFields.choices),
                        blank=True,
                        default=get_default_institution_fields)
    parent = models.ForeignKey("InstitutionGroup",
                               on_delete=models.CASCADE,
                               null=True,
                               blank=True,
                               related_name="children")

    @property
    def institutions_count(self):
        return self.institutions.count()
