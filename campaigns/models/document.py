from django.db import models


class Document(models.Model):
    """
    Document specifies the input data. It can be one field or multiple.
    Document data schema is specified by the Campaign.
    """

    campaign = models.ForeignKey("Campaign",
                                 on_delete=models.CASCADE,
                                 related_name="documents")
    source = models.ForeignKey("Source",
                               on_delete=models.CASCADE,
                               related_name="+")
    data = models.JSONField(default=dict)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
