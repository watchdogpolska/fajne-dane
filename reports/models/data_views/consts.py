from django.db import models
from django.utils.translation import gettext_lazy as _


class AggregationTypes(models.TextChoices):
    SUM = 'SUM', _('Sum')
    AVG = 'AVG', _('Avg')
    COUNT = 'COUNT', _('Count')
    NOTNAN = 'NOTNAN', _('NotNan')



class DataViewTypes(models.TextChoices):
    BASE = 'BASE', _('Base')
    VALUE_COUNTS = 'VALUE_COUNTS', _('Value counts')

