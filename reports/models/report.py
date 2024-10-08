from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from reports.validators.report_layout import validate_report_layout


class ReportStatus(models.TextChoices):
    EMPTY = 'EMPTY', _('Empty')
    IN_PROGRESS = 'IN_PROGRESS', _('In progress')
    READY = 'READY', _('Joined')


class Report(models.Model):
    name = models.CharField(max_length=64)
    status = models.CharField(max_length=12,
                              choices=ReportStatus.choices,
                              default=ReportStatus.EMPTY)
    layout = models.JSONField(default=dict)

    def clean(self):
        validate_report_layout(self.layout)

        ids = set(self.components.values_list('id', flat=True))
        wrong_ids = set(map(int, self.layout.keys())) - ids
        if len(wrong_ids):
            raise ValidationError(f"Wrong components found in the layout: {wrong_ids}")

    def save(self, *args, **kwargs):
        self.clean()
        return super(Report, self).save(*args, **kwargs)
