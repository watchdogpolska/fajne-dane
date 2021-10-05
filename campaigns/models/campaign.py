from typing import Dict

from django.db import models
from django.utils.translation import gettext_lazy as _

from campaigns.models.dto import DocumentDTO
from campaigns.validators.campaign_template import CampaignTemplate
from campaigns.validators.template import validate_campaign_template


class CampaignStatus(models.TextChoices):
    CREATED = 'CREATED', _('Created')
    INITIALIZED = 'INITIALIZED', _('Initialized')
    VALIDATING = 'VALIDATING', _('Validating')
    CLOSED = 'CLOSED', _('Closed')


class Campaign(models.Model):
    """
    Main object.

    After creating status is set to CREATED. schema is empty
    Then you need to upload the schema. Then the set is set to INITIALIZED
    Then you can add documents that follows this schema. You can do them in batch from csv or excel
    or manually using and endpoint
    """

    name = models.CharField(max_length=30, null=False)
    template = models.JSONField(validators=[validate_campaign_template], null=False)
    status = models.CharField(max_length=12,
                              choices=CampaignStatus.choices,
                              default=CampaignStatus.CREATED)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    @property
    def campaign_template(self) -> CampaignTemplate:
        if self.template:
            return CampaignTemplate.from_json(self.template)

    def validate_document(self, document: DocumentDTO):
        self.campaign_template.validate(document)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
