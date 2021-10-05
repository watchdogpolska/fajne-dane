from django.core.exceptions import ValidationError
from django.test import TestCase

from campaigns.validators.schemas import validate_campaign_schema
from campaigns.validators.utils import validate_json_meta_schema
from tests.unit.campaigns.conftest import get_json_test_data


class CampaignValidatorsTestCase(TestCase):
    def setUp(self):
        pass

    def test_json_meta_schema_validation(self):
        with self.assertRaises(ValidationError):
            validate_json_meta_schema({'type': 'object', 'properties': {'value': {'type': 'any'}}})

        validate_json_meta_schema({})

    def test_campaign_schema_validation(self):
        campaign_example = get_json_test_data("campaign_schema_sample.json")
        validate_campaign_schema(campaign_example)

        with self.assertRaises(ValidationError):
            validate_campaign_schema({})
