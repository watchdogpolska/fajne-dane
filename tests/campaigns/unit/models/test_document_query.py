from django.test import TestCase

from campaigns.models import DocumentQuery
from campaigns.models.consts import DocumentQueryStatus, RecordStatus
from tests.campaigns.conftest import basic_document, basic_query, advanced_campaign_with_documents


class DocumentQueryTestCase(TestCase):
    def test_creating(self):
        document = basic_document()
        query = basic_query()

        document_query = DocumentQuery.objects.create(
            document=document,
            query=query
        )
        self.assertIsInstance(document_query, DocumentQuery)
        self.assertEqual(document_query.status, DocumentQueryStatus.CREATED)


class DocumentQueryStatusTestCase(TestCase):
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

        self.assertEqual(dq.status, DocumentQueryStatus.CLOSED)
        dq.accept_records([record])
        dq.refresh_from_db()
        self.assertEqual(dq.status, DocumentQueryStatus.CLOSED)

    def test_accepting_multiple_records(self):
        dq = self.document.document_queries.get(query=self.query_multiple)
        record = dq.records.first()

        self.assertEqual(dq.status, DocumentQueryStatus.CREATED)
        dq.accept_records([record])
        dq.refresh_from_db()
        self.assertEqual(dq.status, DocumentQueryStatus.CLOSED)
