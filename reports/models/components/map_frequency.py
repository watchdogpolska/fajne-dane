from django.db import models

from .consts import ReportComponentTypes
from .data_component import DataComponent


class MapFrequencyComponent(DataComponent):
    title = models.CharField(max_length=256)
    index = models.CharField(max_length=256)
    value = models.CharField(max_length=256)

    def __init__(self, *args, **kwargs):
        if 'type' not in kwargs:
            kwargs['type'] = ReportComponentTypes.MAP_FREQUENCY
        super().__init__(*args, **kwargs)
