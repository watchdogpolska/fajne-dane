from django.db import models
from .source import Source, SourceTypes


class FileSource(Source):
    description = models.TextField(default="", blank=True)
    # url = None
    # file = models.FileField(upload_to='resources') # uploads to S3

    def __init__(self, *args, **kwargs):
        if 'type' not in kwargs:
            kwargs['type'] = SourceTypes.FILE
        super().__init__(*args, **kwargs)
