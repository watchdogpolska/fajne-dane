from typing import Dict

import json
from django.test import TestCase, Client

from campaigns.models import Campaign
from tests.campaigns.conftest import basic_campaign
from tests.conftest import user1, basic_campaign_template
from tests.utils import serialize_date


def campaign_payload() -> Dict:
    return {
        "name": "Test campaign",
        "template": json.dumps(basic_campaign_template())
    }


class CampaignCreateTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_create_campaign(self):
        user = user1(is_active=True, is_staff=True)
        self.client.force_login(user)

        payload = campaign_payload()
        response = self.client.post("/api/v1/campaigns/create/", payload)
        response_data = response.data

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_data['name'], payload['name'])

        campaign = Campaign.objects.get(name=payload['name'])
        self.assertIsInstance(campaign, Campaign)

    def test_create_campaign_no_permission(self):
        user = user1(is_active=True)
        self.client.force_login(user)

        payload = campaign_payload()
        response = self.client.post("/api/v1/campaigns/create/", payload)

        self.assertEqual(response.status_code, 403)


class CampaignListTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_list_campaigns(self):
        user = user1(is_active=True, is_staff=True)
        self.client.force_login(user)
        campaign = basic_campaign()

        response = self.client.get("/api/v1/campaigns/")
        response_data = response.data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response_data[0]['id'], campaign.id)

    def test_list_campaigns_empty(self):
        user = user1(is_active=True, is_staff=True)
        self.client.force_login(user)

        response = self.client.get("/api/v1/campaigns/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [])

    def test_list_campaigns_not_logged(self):
        response = self.client.get("/api/v1/campaigns/")
        self.assertEqual(response.status_code, 200)


class CampaignDetailsTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_get_campaign(self):
        user = user1(is_active=True, is_staff=True)
        self.client.force_login(user)
        
        campaign = basic_campaign()
        response = self.client.get(f"/api/v1/campaigns/{campaign.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {
            "id": campaign.id,
            "name": campaign.name,
            "status": campaign.status,
            "created": serialize_date(campaign.created)
        })

    def test_get_campaign_no_permission(self):
        user = user1(is_active=True, is_staff=False)
        self.client.force_login(user)

        campaign = basic_campaign()
        response = self.client.get(f"/api/v1/campaigns/{campaign.id}/")
        self.assertEqual(response.status_code, 403)

    def test_get_campaign_no_campaign(self):
        user = user1(is_active=True, is_staff=True)
        self.client.force_login(user)

        response = self.client.get(f"/api/v1/campaigns/1/")
        self.assertEqual(response.status_code, 404)

    def test_get_campaign_update(self):
        user = user1(is_active=True, is_staff=True)
        self.client.force_login(user)

        campaign = basic_campaign()
        response = self.client.put(
            f"/api/v1/campaigns/{campaign.id}/",
            data={"name": "Other campaign"},
            content_type='application/json')
        self.assertEqual(response.status_code, 200)

        campaign.refresh_from_db()
        self.assertEqual(campaign.name, "Other campaign")

    def test_get_campaign_delete(self):
        user = user1(is_active=True, is_staff=True)
        self.client.force_login(user)

        campaign = basic_campaign()
        response = self.client.delete(f"/api/v1/campaigns/{campaign.id}/")
        self.assertEqual(response.status_code, 204)
        self.assertIsNone(Campaign.objects.filter(id=campaign.id).first())
