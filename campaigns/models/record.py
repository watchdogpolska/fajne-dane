from django.db import models
from django.utils.translation import gettext_lazy as _


class RecordStatus(models.TextChoices):
    NONE = 'NONE', _('None')
    ACCEPTED = 'ACCEPTED', _('Accepted')
    REJECTED = 'REJECTED', _('Rejected')


class RecordSource(models.TextChoices):
    NONE = 'NONE', _('None')


class Record(models.Model):
    """
    A single answer for a given Query
    """
    query = models.ForeignKey("Query",
                              on_delete=models.CASCADE,
                              related_name="records")
    document = models.ForeignKey("Document",
                                 on_delete=models.CASCADE,
                                 related_name="records")

    value = models.TextField()
    probability = models.FloatField()


    source = models.ForeignKey("Source",
                               on_delete=models.CASCADE,
                               related_name="+")
    status = models.CharField(max_length=10,
                              choices=RecordStatus.choices,
                              default=RecordStatus.NONE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
