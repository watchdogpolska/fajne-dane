from django.db import models
from django.utils.translation import gettext_lazy as _


class ReportStatus(models.TextChoices):
    EMPTY = 'EMPTY', _('Empty')
    IN_PROGRESS = 'IN_PROGRESS', _('In progress')
    READY = 'READY', _('Joined')


class Report(models.Model):
    name = models.CharField(max_length=64)
    status = models.CharField(max_length=12,
                              choices=ReportStatus.choices,
                              default=ReportStatus.EMPTY)
    # layout = models.JSONField(default={})

    def update(self):
        self.status = ReportStatus.IN_PROGRESS
        self.save()
        self._generate()
        self.status = ReportStatus.READY
        self.save()

    def _generate(self):
        ...
