from django.db import models
from django.utils.translation import gettext_lazy as _


class DocumentStatus(models.TextChoices):
    NONE = 'NONE', _('None')
    VALIDATING = 'VALIDATING', _('Validating')
    CLOSED = 'CLOSED', _('Closed')


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
    status = models.CharField(max_length=12,
                              choices=DocumentStatus.choices,
                              default=DocumentStatus.NONE)

    def update_status(self):
        raise NotImplemented()
        # update my status
        self.campaign.update_status()
