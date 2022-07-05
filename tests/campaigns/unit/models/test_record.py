from django.test import TestCase

from campaigns.models import Record
from campaigns.models.consts import RecordStatus
from tests.campaigns.conftest import basic_document_query, basic_user_source, advanced_campaign_with_documents


class RecordTestCase(TestCase):
    def test_creating(self):
        record = Record.objects.create(
            parent=basic_document_query(),
            source=basic_user_source(),
            value="yes",
            probability=0.7
        )
        self.assertIsInstance(record, Record)


class RecordStatusTestCase(TestCase):
    def setUp(self):
        self.campaign = advanced_campaign_with_documents()
        self.document = self.campaign.documents.get(data__institution_id=1425011)
        self.query_single = self.campaign.queries.get(order=0)
        self.query_multiple = self.campaign.queries.get(order=2)

    def test_accepting_single_records(self):
        dq = self.document.document_queries.get(query=self.query_single)
        record = dq.records.first()

        self.assertEqual(record.status, RecordStatus.ACCEPTED)
        record.accept()
        record.refresh_from_db()
        self.assertEqual(record.status, RecordStatus.ACCEPTED)  # this record should be accepted

    def test_accepting_multiple_records(self):
        dq = self.document.document_queries.get(query=self.query_multiple)
        record = dq.records.first()

        record.accept()

        # only one record should be accepted
        self.assertEqual(dq.records.filter(status=RecordStatus.ACCEPTED).count(), 1)
        # all other should be rejected
        self.assertEqual(dq.records.filter(status=RecordStatus.REJECTED).count(), 1)
