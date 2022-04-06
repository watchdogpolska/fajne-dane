from django.db import models, transaction

from campaigns.models.consts import DocumentStatus, RecordStatus, DocumentQueryStatus


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
    institution = models.ForeignKey("Institution",
                                    on_delete=models.CASCADE,
                                    related_name="documents")
    data = models.JSONField(default=dict)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=12,
                              choices=DocumentStatus.choices,
                              default=DocumentStatus.CREATED)

    @transaction.atomic
    def update_status(self):
        """
        Updates document's status based on its document queries.
        """
        last_status = self.status
        if self.status == DocumentStatus.CREATED:  # check if there is at least one document query added
            if self.document_queries.filter(status__in=[
                DocumentQueryStatus.INITIALIZED, DocumentQueryStatus.CLOSED]).count() > 0:
                self.status = DocumentStatus.INITIALIZED

        if self.status == DocumentStatus.INITIALIZED:  # check if one of document query has been closed
            if self.document_queries.filter(status=DocumentQueryStatus.CLOSED).count() > 0:
                self.status = DocumentStatus.VALIDATING

        if self.status == DocumentStatus.VALIDATING:  # every document query has been closed
            if self.document_queries.exclude(status=DocumentQueryStatus.CLOSED).count() == 0:
                self.status = DocumentStatus.CLOSED

        if last_status != self.status:  # check if status has changed
            self.save()

        self.campaign.update_status()  # update campaign status
