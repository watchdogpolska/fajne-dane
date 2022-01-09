from typing import Optional, List
from typing import TYPE_CHECKING

from django.core.exceptions import ValidationError
from django.db import models, transaction

from campaigns.models.consts import CampaignStatus, DocumentStatus
from campaigns.models.dto import DocumentDTO

if TYPE_CHECKING:
    from campaigns.models import DocumentDataField, Query


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

    @transaction.atomic
    def update_status(self):
        """
        Updates campaign status based on the status of its documents.
        """
        last_status = self.status

        if self.status == CampaignStatus.CREATED:
            if self.documents.count() > 0:  # check if at least one document added
                self.status = CampaignStatus.INITIALIZED

        if self.status == CampaignStatus.INITIALIZED:  # at least one document was checked
            if self.documents.exclude(status__in=[DocumentStatus.CREATED, DocumentStatus.INITIALIZED]).count() > 0:
                self.status = CampaignStatus.VALIDATING

        if self.status != CampaignStatus.CREATED:  # all documents are closed
            if self.documents.exclude(status=DocumentStatus.CLOSED).count() == 0:
                self.status = CampaignStatus.CLOSED

        if last_status != self.status:
            self.save()


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
        errors = []
        for field in self.document_fields_objects:
            try:
                field.validate(document)
            except ValidationError as e:
               errors.append(e)

        if validate_records:
            for query in self.queries_objects:
                records = document.records.get(query.name, [])
                for record in records:
                    try:
                        query.validate_record(record)
                    except ValidationError as e:
                        errors.append(e)

        if errors:
            raise ValidationError({"data": errors})
