import json

from django.test import TestCase, Client

from campaigns.validators.template import CAMPAIGN_SCHEMA
from tests.campaigns.conftest import invalid_campaign_template
from tests.conftest import user1, basic_campaign_template


class GetMetaTemplateTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_get_template(self):
        user = user1(is_active=True)
        self.client.force_login(user)
        response = self.client.get("/api/v1/campaigns/template/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {"template": CAMPAIGN_SCHEMA})

    def test_get_template_no_permission(self):
        response = self.client.get("/api/v1/campaigns/template/")
        self.assertEqual(response.status_code, 401)


class ValidateCampaignTemplate(TestCase):
    def setUp(self):
        self.client = Client()

    def test_validate_post_valid(self):
        user = user1(is_active=True)
        self.client.force_login(user)

        payload = json.dumps({"template": basic_campaign_template()})
        response = self.client.post(
            "/api/v1/campaigns/template/validate/", payload,
            content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'is_valid': True, 'errors': []})

    def test_get_template_no_permission(self):
        payload = {"template": basic_campaign_template()}
        response = self.client.post("/api/v1/campaigns/template/validate/", payload)
        self.assertEqual(response.status_code, 401)

    def test_validate_post_invalid(self):
        user = user1(is_active=True)
        self.client.force_login(user)

        payload = json.dumps({"template": invalid_campaign_template()})
        response = self.client.post(
            "/api/v1/campaigns/template/validate/", payload,
            content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {
            'is_valid': False,
            'errors': [
                {'code': "template_error", 'message': "'document' is a required property"},
                {'code': "template_error", 'message': "'queries' is a required property"}
            ]
        })
