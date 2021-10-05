from django.core.exceptions import ValidationError
from django.test import TestCase

from campaigns.models.campaign import Campaign, CampaignStatus
from campaigns.validators.campaign_template import CampaignTemplate
from tests.unit.campaigns.conftest import basic_campaign_template


class CampaignTestCase(TestCase):
    def test_creating_with_empty_schema(self):
        """Tests creating a campaign with empty template."""
        with self.assertRaises(ValidationError):
            Campaign.objects.create(name="test1", template={})

    def test_creating_with_wrong_schema(self):
        """Tests creating a campaign with a template that do not follows the right schema."""
        with self.assertRaises(ValidationError):
            Campaign.objects.create(name="test1", template={"files": []})

    def test_creating(self):
        campaign = Campaign.objects.create(
            name="test1",
            template=basic_campaign_template()
        )
        self.assertEqual(campaign.status, CampaignStatus.CREATED)
        self.assertTrue(type(campaign.campaign_template) is CampaignTemplate)
