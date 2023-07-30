from django.test import TestCase, Client

from campaigns.models import Query
from tests.campaigns.conftest import basic_campaign_with_documents, advanced_campaign_with_documents, basic_campaign
from tests.conftest import user1


class QueryListTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_list_campaigns_queries(self):
        user = user1(is_active=True)
        self.client.force_login(user)
        campaign = basic_campaign_with_documents()
        advanced_campaign_with_documents()

        response = self.client.get(f"/api/v1/campaigns/{campaign.id}/queries/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), campaign.queries.count())
        self.assertTrue(len(response.data) < Query.objects.count())

        response_query_ids = set([d['id'] for d in response.data])
        expected_query_ids = set(campaign.queries.values_list('id', flat=True))
        self.assertEqual(expected_query_ids, response_query_ids)

    def test_list_campaigns_empty(self):
        user = user1(is_active=True, is_staff=True)
        self.client.force_login(user)
        campaign = basic_campaign()
        response = self.client.get(f"/api/v1/campaigns/{campaign.id}/queries/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), campaign.documents.count())
        self.assertEqual(len(response.data), 0)

    def test_list_campaigns_not_logged(self):
        campaign = basic_campaign()
        response = self.client.get(f"/api/v1/campaigns/{campaign.id}/queries/")
        self.assertEqual(response.status_code, 200)


class QueryDetailsTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_query_get(self):
        user = user1(is_active=True, is_staff=True)
        self.client.force_login(user)
        basic_campaign_with_documents()
        query = Query.objects.first()
        response = self.client.get(f"/api/v1/campaigns/queries/{query.id}/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {
            "id": query.id,
            "name": query.name,
            "order": query.order,
            "data": query.data,
            "output_field": {
                "id": query.output_field.id,
                "name": query.output_field.name,
                "widget": query.output_field.widget,
                "answers": query.output_field.answers,
                "metadata": query.output_field.metadata,
                "type": query.output_field.type,
                "validation": query.output_field.validation,
                "default_answer": query.output_field.default_answer
            }
        })

    def test_query_get_no_document(self):
        user = user1(is_active=True, is_staff=True)
        self.client.force_login(user)

        response = self.client.get("/api/v1/campaigns/queries/1/")
        self.assertEqual(response.status_code, 404)

    def test_query_get_no_permission(self):
        user = user1(is_active=True, is_staff=False)
        self.client.force_login(user)
        basic_campaign_with_documents()
        query = Query.objects.first()
        response = self.client.get(f"/api/v1/campaigns/queries/{query.id}/")
        self.assertEqual(response.status_code, 403)

    def test_query_patch(self):
        user = user1(is_active=True, is_staff=True)
        self.client.force_login(user)
        basic_campaign_with_documents()

        query = Query.objects.first()
        response = self.client.patch(
            f"/api/v1/campaigns/queries/{query.id}/",
            data={
                "order": 4,
                "data": {"field": "value"},
            },
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)

        query.refresh_from_db()
        self.assertEqual(query.data, {"field": "value"})
        self.assertEqual(query.order, 4)

    def test_document_delete(self):
        user = user1(is_active=True, is_staff=True)
        self.client.force_login(user)

        basic_campaign_with_documents()
        query = Query.objects.first()
        response = self.client.delete(f"/api/v1/campaigns/queries/{query.id}/")
        self.assertEqual(response.status_code, 204)
        self.assertIsNone(Query.objects.filter(id=query.id).first())



