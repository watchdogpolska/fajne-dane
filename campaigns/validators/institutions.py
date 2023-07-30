import json
from pathlib import Path
from typing import List, Dict

from django.core.exceptions import ValidationError
from jsonschema import Draft7Validator

from campaigns.validators.report import ValidationReport, ValidationError as TemplateValidationError
from campaigns.validators.utils import validate_json_meta_schema


CAMPAIGN_SCHEMA = json.load(open(Path(__file__).resolve().parent / "./schemas/institutions_file-schema.json"))
validate_json_meta_schema(CAMPAIGN_SCHEMA)


def validate_institutions_file(template: Dict):
    validator = Draft7Validator(CAMPAIGN_SCHEMA)
    if errors := sorted(validator.iter_errors(template), key=lambda e: e.path):
        raise ValidationError(errors)


def prepare_validation_report(institutions_list: List[Dict]) -> ValidationReport:
    errors = []
    try:
        validate_institutions_file(institutions_list)
    except ValidationError as exception:
        errors = [
            TemplateValidationError("template_error", e.message.message)
            for e in exception.error_list
        ]
    return ValidationReport(errors=errors)
