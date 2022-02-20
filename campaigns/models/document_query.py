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
    accepted_record = models.OneToOneField("Record", on_delete=models.CASCADE, blank=True, null=True)

    @transaction.atomic
    def update_status(self):
        """
        Updates the status based on its records.
        """
        last_status = self.status
        if self.status == DocumentQueryStatus.CREATED:  # check if at least one record added
            if self.records.count():
                self.status = DocumentQueryStatus.INITIALIZED

        if self.status == DocumentQueryStatus.INITIALIZED:  # check if the record was accepted
            if self.accepted_record:
                self.status = DocumentQueryStatus.CLOSED

        if last_status != self.status:  # check if status has changed
            self.save()

        self.document.update_status()  # update document status

    def accept_record(self, record: "Record"):
        self.records.exclude(id=record.id).update(status=RecordStatus.REJECTED)
        record.status = RecordStatus.ACCEPTED
        record.save()
        self.accepted_record = record
        self.save()
        self.update_status()
