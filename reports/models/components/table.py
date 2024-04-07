from django.contrib.postgres.fields import ArrayField
from django.db import models

from .consts import ReportComponentTypes
from .data_component import DataComponent


class TableComponent(DataComponent):
    title = models.CharField(max_length=256, blank=True, null=True)
    columns = ArrayField(models.CharField(max_length=256), default=list)

    def __init__(self, *args, **kwargs):
        if 'type' not in kwargs:
            kwargs['type'] = ReportComponentTypes.TABLE
        super().__init__(*args, **kwargs)
