from django.db import models
from django.contrib.postgres.fields import ArrayField


class OutputField(models.Model):
    """
    """

    name = models.CharField(max_length=64)
    widget = models.CharField(max_length=64)
    answers = ArrayField(models.TextField())
    type = models.CharField(max_length=10)
    validation = models.BooleanField(default=False)
    default_answer = models.TextField(default=None, null=True)
