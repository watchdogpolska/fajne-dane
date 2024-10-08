from django.test import TestCase, Client

from campaigns.models import Document, Institution
from campaigns.models.consts import DocumentStatus
from tests.campaigns.conftest import (
    basic_campaign_with_documents, advanced_campaign_with_documents, basic_campaign, basic_institution
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

        response_document_ids = {d['id'] for d in response.data}
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
            'status': document.status,
            'source': {
                'id': source.id,
                'name': source.name,
                'type': source.type
            },
            'institution': {
                'id': document.institution.id,
                'key': document.institution.key,
                'name': document.institution.name,
            },
            'document_queries': [
                {
                    "id": dq.id,
                    "query": {
                        "id": dq.query.id,
                        "order": dq.query.order,
                        "name": dq.query.name,
                        "data": dq.query.data
                    },
                    "status": dq.status
                }
                for dq in document.document_queries.all()
            ],
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
        advanced_campaign_with_documents()

        document = Document.objects.first()
        response = self.client.put(
            f"/api/v1/campaigns/documents/{document.id}/",
            data={"data": {"document_url": "value"}},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)

        document.refresh_from_db()
        self.assertEqual(document.data, {"document_url": "value"})

    def test_document_put_validation(self):
        user = user1(is_active=True, is_staff=True)
        self.client.force_login(user)
        basic_campaign_with_documents()

        document = Document.objects.first()
        response = self.client.put(
            f"/api/v1/campaigns/documents/{document.id}/",
            data={"data": {"institution_id": "value"}},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(len(response.data['data']), 1),
        self.assertEqual(str(response.data['data'][0]),
                         "Found invalid fields in the document: {'institution_id'}")

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

        campaign = advanced_campaign_with_documents()
        institution = Institution.objects.first()
        response = self.client.post(
            f"/api/v1/campaigns/{campaign.id}/documents/create/",
            data={
                "institution": institution.id,
                "data": {"document_url": "1"},
                "campaign": campaign.id
            },
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)

        document = Document.objects.get(id=response.data['id'])
        source = document.source.to_child()
        self.assertEqual(source.user, user)
        self.assertEqual(document.data, {"document_url": '1'})
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


class DocumentBulkDeleteTestCase(TestCase):
    def setUp(self):
        self.client = Client()


    def test_document_delete_one(self):
        campaign = basic_campaign_with_documents()
        user = user1(is_active=True, is_staff=True)
        self.client.force_login(user)

        assert campaign.documents.count() == 4

        document = campaign.documents.first()
        response = self.client.post(
            f"/api/v1/campaigns/{campaign.id}/documents/delete/",
            data={"ids": [document.id]},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 204)

        assert campaign.documents.count() == 3


    def test_document_delete_many(self):
        campaign = basic_campaign_with_documents()
        user = user1(is_active=True, is_staff=True)
        self.client.force_login(user)

        assert campaign.documents.count() == 4

        documents = campaign.documents.all()[:2]
        response = self.client.post(
            f"/api/v1/campaigns/{campaign.id}/documents/delete/",
            data={"ids": [doc.id for doc in documents]},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 204)

        assert campaign.documents.count() == 2


class GetUnsolvedDocumentTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_document_get(self):
        user = user1(is_active=True, is_staff=True)
        self.client.force_login(user)
        campaign = basic_campaign_with_documents()
        response = self.client.get(f"/api/v1/campaigns/{campaign.id}/documents/next/")
        document = campaign.documents.exclude(status__in=[DocumentStatus.CLOSED]).first()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {
            "id": document.id
        })
