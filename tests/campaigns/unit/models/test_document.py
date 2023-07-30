from django.test import TestCase

from campaigns.models import Document
from campaigns.models.consts import DocumentStatus, RecordStatus
from tests.campaigns.conftest import (
    basic_campaign, basic_file_source, advanced_campaign_with_documents, basic_institution
)


class DocumentTestCase(TestCase):
    def test_creating(self):
        campaign = basic_campaign()
        document = Document.objects.create(
            campaign=campaign,
            source=basic_file_source(campaign),
            data={"meta": 1},
            institution=basic_institution()
        )
        self.assertIsInstance(document, Document)


class DocumentAdvancedStatusTestCase(TestCase):
    def setUp(self):
        self.campaign = advanced_campaign_with_documents()
        self.document = self.campaign.documents.get(institution__key="1425011")
        self.query_single = self.campaign.queries.get(order=0)
        self.query_multiple = self.campaign.queries.get(order=2)

        # reject all records
        for dq in self.document.document_queries.all():
            dq.records.update(status=RecordStatus.REJECTED)

    def test_accepting_single_records(self):
        dq = self.document.document_queries.get(query=self.query_single)
        record = dq.records.first()

        document = self.document
        self.assertEqual(document.status, DocumentStatus.VALIDATING)
        dq.accept_records([record])
        document.refresh_from_db()
        self.assertEqual(document.status, DocumentStatus.VALIDATING)

    def test_accepting_multiple_records(self):
        dq = self.document.document_queries.get(query=self.query_multiple)
        record = dq.records.first()

        document = self.document
        self.assertEqual(document.status, DocumentStatus.VALIDATING)
        dq.accept_records([record])
        document.refresh_from_db()
        self.assertEqual(document.status, DocumentStatus.CLOSED)

    def test_close_document(self):
        document = self.document
        self.assertEqual(document.status, DocumentStatus.VALIDATING)

        for dq in self.document.document_queries.all():
            record = dq.records.first()
            dq.accept_records([record])

        document.refresh_from_db()
        self.assertEqual(document.status, DocumentStatus.CLOSED)
