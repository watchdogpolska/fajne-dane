from django.core.exceptions import ValidationError
from django.test import TestCase

from campaigns.validators.template import validate_campaign_template, prepare_validation_report
from campaigns.validators.report import ValidationReport, ValidationError as TemplateValidationError
from campaigns.validators.utils import validate_json_meta_schema
from tests.campaigns.conftest import invalid_campaign_template
from tests.conftest import basic_campaign_template, advanced_campaign_template


class CampaignTemplateValidatorsTestCase(TestCase):
    def test_json_meta_schema_validation_invalid(self):
        with self.assertRaises(ValidationError):
            validate_json_meta_schema(invalid_campaign_template())

    def test_json_meta_schema_validation_empty(self):
        try:
            validate_json_meta_schema({})
        except ValidationError:
            self.fail()

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


class CampaignValidationReportTestCase(TestCase):
    def test_create_validation_error(self):
        error = TemplateValidationError("code", "message")
        self.assertIsInstance(error, TemplateValidationError)
        self.assertEqual(error.code, "code")
        self.assertEqual(error.message, "message")

    def test_create_validation_report_valid(self):
        report = ValidationReport([])
        self.assertTrue(report.is_valid)
        self.assertEqual(len(report.errors), 0)

    def test_create_validation_report_invalid(self):
        report = ValidationReport(
            errors=[TemplateValidationError("code", "message")]
        )
        self.assertFalse(report.is_valid)
        self.assertEqual(len(report.errors), 1)


class PrepareValidationReportTestCase(TestCase):
    def test_prepare_validation_error_valid(self):
        report = prepare_validation_report(basic_campaign_template())
        self.assertIsInstance(report, ValidationReport)
        self.assertTrue(report.is_valid)

    def test_prepare_validation_error_invalid(self):
        report = prepare_validation_report(invalid_campaign_template())
        self.assertIsInstance(report, ValidationReport)
        self.assertFalse(report.is_valid)
        self.assertEqual(report.errors, [
            TemplateValidationError(code='template_error', message="'document' is a required property"),
            TemplateValidationError(code='template_error', message="'queries' is a required property")
        ])
