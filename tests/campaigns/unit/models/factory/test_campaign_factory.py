from django.core.exceptions import ValidationError
from django.test import TestCase

from campaigns.models import Campaign
from campaigns.models.factory import campaign_factory
from tests.conftest import basic_campaign_template, advanced_campaign_template


class CampaignFactoryTestCase(TestCase):

    def test_creating_basic_campaign(self):
        """Tests creating a campaign with a correct template."""
        campaign = campaign_factory.create("test", basic_campaign_template())
        self.assertIsInstance(campaign, Campaign)
        self.assertTrue(campaign.document_fields.count() == 0)
        self.assertTrue(campaign.queries.count() == 1)

        query = campaign.queries.first()
        self.assertEqual(query.order, 0)
        self.assertEqual(query.name, "Question 0")
        self.assertEqual(query.data, [
            {
                "name": "question",
                "value": "What is it?",
                "type": "str",
                "widget": "label"
            }
        ])

        output_field = query.output_field
        self.assertEqual(output_field.name, "answer")
        self.assertEqual(output_field.widget, "ChoiceField")
        self.assertEqual(output_field.answers, ["yes", "no"])
        self.assertEqual(output_field.metadata, {})
        self.assertEqual(output_field.type, "str")
        self.assertEqual(output_field.validation, True)
        self.assertEqual(output_field.default_answer, 1)

    def test_creating_campaign_wrong_template(self):
        """Tests creating a campaign with a wrong template."""
        with self.assertRaises(ValidationError):
            campaign_factory.create("test", {})

    def test_creating_advanced_campaign(self):
        """Tests creating a campaign with an advanced template."""
        try:
            campaign_factory.create("test", advanced_campaign_template())
        except ValidationError:
            self.fail()
