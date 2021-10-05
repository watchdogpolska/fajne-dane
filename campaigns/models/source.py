from django.db import models


class Source(models.Model):
    campaign = None
    name = models.CharField(max_length=30)


class Resource(Source):
    description = None
    url = None
    # file = models.FileField(upload_to='resources') # uploads to S3


    pass


class ManualSource(Source):
    pass
