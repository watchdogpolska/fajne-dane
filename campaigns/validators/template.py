import json
from pathlib import Path
from typing import Dict

from django.core.exceptions import ValidationError
from jsonschema import Draft7Validator

from campaigns.validators.report import ValidationReport, ValidationError as TemplateValidationError
from fajne_dane.core.utils.validators import validate_json_meta_schema


CAMPAIGN_SCHEMA = json.load(open(Path(__file__).resolve().parent / "./schemas/campaign_template-schema.json"))
validate_json_meta_schema(CAMPAIGN_SCHEMA)


def validate_campaign_template(template: Dict):
    validator = Draft7Validator(CAMPAIGN_SCHEMA)
    errors = sorted(validator.iter_errors(template), key=lambda e: e.path)
    if errors:
        raise ValidationError(errors)


def prepare_validation_report(template: Dict) -> ValidationReport:
    errors = []
    try:
        validate_campaign_template(template)
    except ValidationError as exception:
        errors = [
            TemplateValidationError("template_error", e.message.message)
            for e in exception.error_list
        ]
    return ValidationReport(errors=errors)
