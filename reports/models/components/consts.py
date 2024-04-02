from django.db import models
from django.utils.translation import gettext_lazy as _


class ReportComponentTypes(models.TextChoices):
    TABLE = 'TABLE', _('Table')
    BAR_PLOT = 'BAR_PLOT', _('Bar plot')
    HEADER = 'HEADER', _('Header')
    HTML = 'HTML', _('HTML')
    MAP_FREQUENCY = 'MAP_FREQUENCY', _('Map frequency')
    REFERENCES = 'REFERENCES', _('References')
