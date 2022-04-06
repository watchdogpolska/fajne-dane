from django.test import TestCase

from campaigns.models import Document
from campaigns.models.consts import DocumentStatus
from tests.campaigns.conftest import basic_campaign, basic_file_source, advanced_campaign_with_documents, \
    basic_institution


class DocumentTestCase(TestCase):
    def test_creating(self):
        campaign = basic_campaign()
        document = Document.objects.create(
            campaign=campaign,
            source=basic_file_source(campaign),
            data={"institution_id": 1},
            institution=basic_institution()
        )
        self.assertIsInstance(document, Document)


class DocumentAdvancedStatusTestCase(TestCase):
    def setUp(self):
        self.campaign = advanced_campaign_with_documents()
        self.document = self.campaign.documents.get(data__institution_id=1425011)
        self.query_single = self.campaign.queries.get(order=0)
        self.query_multiple = self.campaign.queries.get(order=2)

    def test_accepting_single_records(self):
        dq = self.document.document_queries.get(query=self.query_single)
        record = dq.records.first()

        document = self.document
        self.assertEqual(document.status, DocumentStatus.INITIALIZED)
        record.accept()
        document.refresh_from_db()
        self.assertEqual(document.status, DocumentStatus.VALIDATING)

    def test_accepting_multiple_records(self):
        dq = self.document.document_queries.get(query=self.query_multiple)
        record = dq.records.first()

        document = self.document
        self.assertEqual(document.status, DocumentStatus.INITIALIZED)
        record.accept()
        document.refresh_from_db()
        self.assertEqual(document.status, DocumentStatus.VALIDATING)

    def test_close_document(self):
        document = self.document
        self.assertEqual(document.status, DocumentStatus.INITIALIZED)

        for dq in self.document.document_queries.all():
            record = dq.records.first()
            record.accept()

        document.refresh_from_db()
        self.assertEqual(document.status, DocumentStatus.CLOSED)
