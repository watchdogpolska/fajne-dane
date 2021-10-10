from typing import TYPE_CHECKING

from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from campaigns.models.dto import RecordDTO
from campaigns.validators.type import validate_type


class OutputField(models.Model):
    """
    """

    name = models.CharField(max_length=64)
    widget = models.CharField(max_length=64)
    answers = ArrayField(models.TextField(), null=True, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    type = models.CharField(max_length=10)
    validation = models.BooleanField(default=False)
    default_answer = models.IntegerField(default=None, null=True, blank=True)

    def validate(self, record: RecordDTO):
        errors = []
        try:
            validate_type(record.value, self.type)
        except ValidationError as e:
            errors.append(e)

        if self.answers:
            if self.validation and record.value not in self.answers:
                errors.append(
                    ValidationError(
                        _("Record value: '%(value)s' not found in the list of accepted answers."),
                        code='invalid-value',
                        params={'value': record.value}
                    )
                )
        if errors:
            raise ValidationError(errors)
