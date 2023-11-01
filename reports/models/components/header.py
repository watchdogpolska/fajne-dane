from django.db import models

from .component import ReportComponent
from .consts import ReportComponentTypes


class HeaderComponent(ReportComponent):
    title = models.CharField(max_length=256)
    subtitle = models.CharField(max_length=512)

    def __init__(self, *args, **kwargs):
        if 'type' not in kwargs:
            kwargs['type'] = ReportComponentTypes.HEADER
        super().__init__(*args, **kwargs)
