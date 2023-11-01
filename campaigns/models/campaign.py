from typing import Optional, List
from typing import TYPE_CHECKING

from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.utils.translation import gettext_lazy as _

from campaigns.models.consts import CampaignStatus, DocumentStatus
from campaigns.models.dto import DocumentDTO

if TYPE_CHECKING:
    from campaigns.models import DocumentDataField, Query


def get_institution_groups_path(group_id: int) -> List[int]:
    import campaigns.models.institutions.instituion_group as g
    mapping = {i['id']: i['parent_id'] for i in g.InstitutionGroup.objects.values("id", "parent_id")}
    path = [group_id]
    while group_id:
        group_id = mapping[group_id]
        path.append(group_id)
    return path[:-1]


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

    institution_group = models.ForeignKey("InstitutionGroup",
                                          on_delete=models.CASCADE,
                                          null=True,
                                          related_name="campaigns")


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._document_fields_objects = None
        self._queries_objects = None
        self._institution_groups_path = None

    @transaction.atomic
    def update_status(self):
        """
        Updates campaign status based on the status of its documents.
        """
        last_status = self.status

        if self.status == CampaignStatus.CREATED \
                and self.documents.count() > 0:
            self.status = CampaignStatus.VALIDATING

        if self.status != CampaignStatus.CREATED \
                    and self.documents.exclude(status=DocumentStatus.CLOSED).count() == 0:
            self.status = CampaignStatus.CLOSED

        if last_status != self.status:
            self.save()

    def update_data_source(self):
        self.datasource.update()

    def mark_data_source(self):
        self.datasource.mark()

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

    @property
    def institution_groups_path(self) -> List[int]:
        """Prepares a list containing a full path of institution groups path"""
        if not self._institution_groups_path:
            self._institution_groups_path = get_institution_groups_path(self.institution_group.id)
        return self._institution_groups_path


    def validate_document(self, document: DocumentDTO, validate_records: Optional[bool]=True):
        """
        Validates Document's data using  DocumentTemplate from Campaign's template

        :raises: ValidationError
        """
        errors = []

        valid_names = set()
        for field in self.document_fields_objects:
            try:
                field.validate(document)
                valid_names.add(field.name)
            except ValidationError as e:
                errors.append(e)

        # check if document institution is in the right group

        if additional_fields := set(document.data.keys()) - valid_names:
            errors.append(
                ValidationError(
                    _("Found invalid fields in the document: %(value)s"),
                    code="invalid-fields",
                    params={"value": additional_fields},
                )
            )

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
