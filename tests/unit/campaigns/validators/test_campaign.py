from django.core.exceptions import ValidationError
from django.test import TestCase

from campaigns.validators.template import validate_campaign_template
from campaigns.validators.utils import validate_json_meta_schema
from tests.unit.campaigns.conftest import basic_campaign_template, advanced_campaign_template


class CampaignValidatorsTestCase(TestCase):
    def test_json_meta_schema_validation(self):
        with self.assertRaises(ValidationError):
            validate_json_meta_schema({'type': 'object', 'properties': {'value': {'type': 'any'}}})

        validate_json_meta_schema({})

    def test_basic_campaign_template_validation(self):
        try:
            validate_campaign_template(basic_campaign_template())
        except ValidationError:
            self.fail()

    def test_advanced_campaign_template_validation(self):
        try:
            validate_campaign_template(advanced_campaign_template())
        except ValidationError:
            self.fail()

    def test_campaign_template_validation_empty(self):
        with self.assertRaises(ValidationError):
            validate_campaign_template({})
