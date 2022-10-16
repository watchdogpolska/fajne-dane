from django.db import models


class InstitutionGroup(models.Model):
    """
    """
    name = models.CharField(max_length=64)

    parent = models.ForeignKey("InstitutionGroup",
                               on_delete=models.CASCADE,
                               null=True,
                               blank=True,
                               related_name="children")
