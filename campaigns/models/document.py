from django.db import models

from campaigns.models.dto import DocumentDTO


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

    def clean(self):
        cleaned_data = super().clean()
        if hasattr(self, 'campaign'):
            template = self.campaign.campaign_template
            template.document_template.validate_data(self.data)

        return cleaned_data

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
