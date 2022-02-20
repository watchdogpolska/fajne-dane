from django.db import models


class Institution(models.Model):
    """
    """

    key = models.CharField(max_length=64)
    name = models.CharField(max_length=64)
