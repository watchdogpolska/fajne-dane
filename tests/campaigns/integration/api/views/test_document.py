from django.test import TestCase, Client

from campaigns.models import Document
from tests.campaigns.conftest import (
    basic_campaign_with_documents, advanced_campaign_with_documents, basic_campaign
)
from tests.conftest import user1
from tests.utils import serialize_date


class DocumentListTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_list_campaigns_documents(self):
        user = user1(is_active=True, is_staff=True)
        self.client.force_login(user)
        campaign = basic_campaign_with_documents()
        advanced_campaign_with_documents()

        response = self.client.get(f"/api/v1/campaigns/{campaign.id}/documents/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), campaign.documents.count())
        self.assertTrue(len(response.data) < Document.objects.count())

        response_document_ids = set([d['id'] for d in response.data])
        expected_document_ids = set(campaign.documents.values_list('id', flat=True))
        self.assertEqual(expected_document_ids, response_document_ids)

    def test_list_campaigns_empty(self):
        user = user1(is_active=True, is_staff=True)
        self.client.force_login(user)
        campaign = basic_campaign()
        response = self.client.get(f"/api/v1/campaigns/{campaign.id}/documents/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), campaign.documents.count())
        self.assertEqual(len(response.data), 0)

    def test_list_campaigns_not_logged(self):
        campaign = basic_campaign()
        response = self.client.get(f"/api/v1/campaigns/{campaign.id}/documents/")
        self.assertEqual(response.status_code, 200)


class DocumentDetailsTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_document_get(self):
        user = user1(is_active=True, is_staff=True)
        self.client.force_login(user)
        basic_campaign_with_documents()
        document = Document.objects.first()
        response = self.client.get(f"/api/v1/campaigns/documents/{document.id}/")

        self.assertEqual(response.status_code, 200)
        source = document.source.to_child()
        self.assertEqual(response.data, {
            "id": document.id,
            'data': document.data,
            'status': 'NONE',
            'source': {
                'id': source.id,
                'name': source.name,
                'description': source.description,
                'file': None
            },
            'created': serialize_date(document.created)
        })

    def test_document_get_no_document(self):
        user = user1(is_active=True, is_staff=True)
        self.client.force_login(user)

        response = self.client.get("/api/v1/campaigns/documents/1/")
        self.assertEqual(response.status_code, 404)

    def test_document_get_no_permission(self):
        user = user1(is_active=True, is_staff=False)
        self.client.force_login(user)
        basic_campaign_with_documents()
        document = Document.objects.first()
        response = self.client.get(f"/api/v1/campaigns/documents/{document.id}/")
        self.assertEqual(response.status_code, 403)

    def test_document_put(self):
        user = user1(is_active=True, is_staff=True)
        self.client.force_login(user)
        basic_campaign_with_documents()

        document = Document.objects.first()
        response = self.client.put(
            f"/api/v1/campaigns/documents/{document.id}/",
            data={"data": {"institution_id": "value"}},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)

        document.refresh_from_db()
        self.assertEqual(document.data, {"institution_id": "value"})

    def test_document_put_validation(self):
        user = user1(is_active=True, is_staff=True)
        self.client.force_login(user)
        basic_campaign_with_documents()

        document = Document.objects.first()
        response = self.client.put(
            f"/api/v1/campaigns/documents/{document.id}/",
            data={"data": {"value": "value"}},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(len(response.data['data']), 1),
        self.assertEqual(str(response.data['data'][0]),
                         "Field: 'institution_id' not found in the document data.")

    def test_document_delete(self):
        user = user1(is_active=True, is_staff=True)
        self.client.force_login(user)

        basic_campaign_with_documents()
        document = Document.objects.first()
        response = self.client.delete(f"/api/v1/campaigns/documents/{document.id}/")
        self.assertEqual(response.status_code, 204)
        self.assertIsNone(Document.objects.filter(id=document.id).first())


class DocumentCreateTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_document_create(self):
        user = user1(is_active=True, is_staff=True)
        self.client.force_login(user)

        campaign = basic_campaign_with_documents()
        response = self.client.post(
            f"/api/v1/campaigns/{campaign.id}/documents/create/",
            data={
                "data": {"institution_id": "1"},
                "campaign": campaign.id
            },
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)

        document = Document.objects.get(id=response.data['id'])
        source = document.source.to_child()
        self.assertEqual(source.user, user)
        self.assertEqual(document.data, {"institution_id": '1'})
        self.assertEqual(document.campaign, campaign)

    def test_document_create_no_permission(self):
        user = user1(is_active=True, is_staff=False)
        self.client.force_login(user)

        campaign = basic_campaign_with_documents()
        response = self.client.post(
            f"/api/v1/campaigns/{campaign.id}/documents/create/",
            data={"data": {"institution_id": "1"}},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 403)
