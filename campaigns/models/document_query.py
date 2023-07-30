from typing import List

from django.db import models, transaction

from campaigns.models.consts import RecordStatus, DocumentQueryStatus


class DocumentQuery(models.Model):
    """
    Stores information about all records for given query and document.
    """

    query = models.ForeignKey("Query",
                              on_delete=models.CASCADE,
                              related_name="document_queries")
    document = models.ForeignKey("Document",
                                 on_delete=models.CASCADE,
                                 related_name="document_queries")


    status = models.CharField(max_length=12,
                              choices=DocumentQueryStatus.choices,
                              default=DocumentQueryStatus.CREATED)

    @transaction.atomic
    def update_status(self):
        """
        Updates the status based on its records.
        """
        last_status = self.status
        if self.accepted_records.count() > 0:
            self.status = DocumentQueryStatus.CLOSED

        if last_status != self.status:  # check if status has changed
            self.save()

        self.document.update_status()  # update document status

    @property
    def accepted_records(self) -> List["Record"]:
        return self.records.filter(status=RecordStatus.ACCEPTED)

    def accept_records(self, records: List["Record"]):
        records_ids = [r.id for r in records]
        self.records.exclude(id__in=records_ids).update(status=RecordStatus.REJECTED)
        self.records.filter(id__in=records_ids).update(status=RecordStatus.ACCEPTED)
        self.update_status()
