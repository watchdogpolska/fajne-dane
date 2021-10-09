from django.core.exceptions import ValidationError
from django.test import TestCase

from campaigns.models import Document
from campaigns.models.campaign import Campaign, CampaignStatus
from campaigns.models.dto import DocumentDTO, RecordDTO
from campaigns.validators.campaign_template import CampaignTemplate
from tests.unit.campaigns.conftest import basic_campaign_template
from tests.unit.campaigns.models.conftest import basic_campaign, basic_campaign_with_queries


class CampaignTestCase(TestCase):

    def test_creating_with_empty_template(self):
        """Tests creating a campaign with a template."""
        campaign = Campaign.objects.create(name="test1", template=basic_campaign_template())
        self.assertIsInstance(campaign, Campaign)

    def test_creating(self):
        campaign = basic_campaign()
        self.assertEqual(campaign.status, CampaignStatus.CREATED)
        self.assertIsInstance(campaign.template, dict)

    def test_validating_correct_document(self):
        campaign = basic_campaign_with_queries()
        try:
            campaign.validate_document(
                DocumentDTO(
                    data={"institution_id": 1}
                )
            )
        except ValidationError:
            self.fail()

    def test_validating_correct_document_with_record(self):
        campaign = basic_campaign_with_queries()
        try:
            campaign.validate_document(
                DocumentDTO(
                    data={"institution_id": 1},
                    records={
                        "question": RecordDTO(
                            value="yes",
                            probability=0.4
                        )
                    }
                )
            )
        except ValidationError:
            self.fail()

    def test_validating_wrong_document(self):
        campaign = basic_campaign_with_queries()
        with self.assertRaises(ValidationError):
            campaign.validate_document(
                DocumentDTO(
                    data={"project_id": 1}
                )
            )

    def test_validating_correct_document_wrong_record(self):
        campaign = basic_campaign_with_queries()
        with self.assertRaises(ValidationError):
            campaign.validate_document(
                DocumentDTO(
                    data={"institution_id": 1},
                    records={
                        "Question 0": RecordDTO(
                            value="maybe",
                            probability=0.4
                        )
                    }
                )
            )
