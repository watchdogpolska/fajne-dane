from django.db import models, transaction

from campaigns.models.consts import RecordStatus


class Record(models.Model):
    """
    A single answer for a given Query
    """
    value = models.TextField()
    probability = models.FloatField()

    parent = models.ForeignKey("DocumentQuery",
                               on_delete=models.CASCADE,
                               related_name="records")

    source = models.ForeignKey("Source",
                               on_delete=models.CASCADE,
                               related_name="+")
    status = models.CharField(max_length=10,
                              choices=RecordStatus.choices,
                              default=RecordStatus.NONE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
