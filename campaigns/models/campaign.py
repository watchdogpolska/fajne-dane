from typing import Optional, List

from django.db import models
from django.utils.translation import gettext_lazy as _

from campaigns.models.dto import DocumentDTO

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from campaigns.models import DocumentDataField, Query


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

    name = models.CharField(max_length=30, null=False, unique=True)
    template = models.JSONField(null=False)
    status = models.CharField(max_length=12,
                              choices=CampaignStatus.choices,
                              default=CampaignStatus.CREATED)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._document_fields_objects = None
        self._queries_objects = None

    @property
    def document_fields_objects(self) -> List["DocumentDataField"]:
        """Documents fields objects cached for optimizing validation time."""
        if not self._document_fields_objects:
            self._document_fields_objects = list(self.document_fields.all())
        return self._document_fields_objects

    @property
    def queries_objects(self) -> List["Query"]:
        """Queries objects cached for optimizing validation time."""
        if not self._queries_objects:
            self._queries_objects = list(self.queries.all())
        return self._queries_objects

    def validate_document(self, document: DocumentDTO, validate_records: Optional[bool]=True):
        """
        Validates Document's data using  DocumentTemplate from Campaign's template

        :raises: ValidationError
        """
        for field in self.document_fields_objects:
            field.validate(document)

        if validate_records:
            for query in self.queries_objects:
                record = document.records.get(query.name)
                if not record:
                    continue
                query.validate(record)
