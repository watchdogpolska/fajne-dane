from django.test import TestCase, Client

from campaigns.models import Record
from campaigns.models.record import RecordStatus
from tests.campaigns.conftest import (
    basic_campaign_with_documents, basic_campaign
)
from tests.conftest import user1


class RecordListTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_list_documents_records(self):
        user = user1(is_active=True, is_staff=False)
        self.client.force_login(user)
        campaign = basic_campaign_with_documents()
        document = campaign.documents.first()

        response = self.client.get(f"/api/v1/campaigns/documents/{document.id}/records/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), document.records.count())
        self.assertTrue(len(response.data) < Record.objects.count())

        response_records_ids = set([d['id'] for d in response.data])
        expected_records_ids = set(document.records.values_list('id', flat=True))
        self.assertEqual(expected_records_ids, response_records_ids)

    def test_list_records_empty(self):
        user = user1(is_active=True, is_staff=True)
        self.client.force_login(user)
        campaign = basic_campaign_with_documents()
        document = campaign.documents.first()
        document.records.all().delete()

        response = self.client.get(f"/api/v1/campaigns/documents/{document.id}/records/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), document.records.count())
        self.assertEqual(len(response.data), 0)

    def test_list_campaigns_not_logged(self):
        campaign = basic_campaign_with_documents()
        document = campaign.documents.first()
        response = self.client.get(f"/api/v1/campaigns/documents/{document.id}/records/")
        self.assertEqual(response.status_code, 200)


class RecordDetailsTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_record_get(self):
        user = user1(is_active=True, is_staff=True)
        self.client.force_login(user)
        basic_campaign_with_documents()
        record = Record.objects.first()
        source = record.source.to_child()

        response = self.client.get(f"/api/v1/campaigns/records/{record.id}/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {
            "id": record.id,
            "value": record.value,
            "probability": record.probability,
            "source": {
                "id": source.id,
                "name": source.name,
                "description": source.description,
                'source': source.source,
                "file": None
            },
            "status": record.status
        })

    def test_record_get_no_record(self):
        user = user1(is_active=True, is_staff=True)
        self.client.force_login(user)

        response = self.client.get("/api/v1/campaigns/records/1/")
        self.assertEqual(response.status_code, 404)

    def test_record_get_no_permission(self):
        user = user1(is_active=True, is_staff=False)
        self.client.force_login(user)
        basic_campaign_with_documents()
        record = Record.objects.first()
        response = self.client.get(f"/api/v1/campaigns/records/{record.id}/")
        self.assertEqual(response.status_code, 403)

    def test_query_patch(self):
        user = user1(is_active=True, is_staff=True)
        self.client.force_login(user)
        basic_campaign_with_documents()

        record = Record.objects.first()
        response = self.client.patch(
            f"/api/v1/campaigns/records/{record.id}/",
            data={
                "probability": 0.0,
                "status": "ACCEPTED"
            },
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)

        record.refresh_from_db()
        self.assertEqual(record.probability, 0.0)
        self.assertEqual(record.status, RecordStatus.ACCEPTED)

    def test_document_delete(self):
        user = user1(is_active=True, is_staff=True)
        self.client.force_login(user)

        basic_campaign_with_documents()
        record = Record.objects.first()
        response = self.client.delete(f"/api/v1/campaigns/records/{record.id}/")
        self.assertEqual(response.status_code, 204)
        self.assertIsNone(Record.objects.filter(id=record.id).first())


class RecordCreateTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_record_create(self):
        user = user1(is_active=True, is_staff=True)
        self.client.force_login(user)

        campaign = basic_campaign_with_documents()
        document = campaign.documents.first()
        query = campaign.queries.first()

        response = self.client.post(
            f"/api/v1/campaigns/documents/{document.id}/records/create/",
            data={
                "query": query.id,
                "value": "yes",
                "probability": 0.3
            },
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)

        record = Record.objects.get(id=response.data['id'])
        source = record.source.to_child()
        self.assertEqual(source.user, user)
        self.assertEqual(record.value, "yes")
        self.assertEqual(record.probability, 0.3)
        self.assertEqual(record.query, query)
        self.assertEqual(record.document, document)

    def test_record_create_wrong_value(self):
        user = user1(is_active=True, is_staff=True)
        self.client.force_login(user)

        campaign = basic_campaign_with_documents()
        document = campaign.documents.first()
        query = campaign.queries.first()

        response = self.client.post(
            f"/api/v1/campaigns/documents/{document.id}/records/create/",
            data={
                "query": query.id,
                "value": "other",
                "probability": 0.3
            },
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(len(response.data['value']), 1),
        self.assertEqual(str(response.data['value'][0]),
                         "Record value: 'other' not found in the list of accepted answers.")

    def test_record_query_no_permission(self):
        user = user1(is_active=True, is_staff=False)
        self.client.force_login(user)

        campaign = basic_campaign_with_documents()
        document = campaign.documents.first()
        query = campaign.queries.first()

        response = self.client.post(
            f"/api/v1/campaigns/documents/{document.id}/records/create/",
            data={
                "query": query.id,
                "value": "yes",
                "probability": 0.3
            },
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 403)
