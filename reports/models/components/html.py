from django.db import models

from .component import ReportComponent
from .consts import ReportComponentTypes


class HTMLComponent(ReportComponent):
    text = models.TextField()

    def __init__(self, *args, **kwargs):
        if 'type' not in kwargs:
            kwargs['type'] = ReportComponentTypes.HTML
        super().__init__(*args, **kwargs)
