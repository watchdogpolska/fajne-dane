import json
from dataclasses import dataclass
from typing import Dict, List

from django.core.exceptions import ValidationError
from jsonschema import Draft7Validator

from campaigns.validators.utils import validate_json_meta_schema
from pathlib import Path

CAMPAIGN_SCHEMA = json.load(open(Path(__file__).resolve().parent / "./schemas/campaign_template-schema.json"))
validate_json_meta_schema(CAMPAIGN_SCHEMA)


@dataclass
class TemplateValidationError:
    code: str
    message: str

    def to_json(self):
        return { "code": self.code, "message": self.message }


@dataclass
class TemplateValidationReport:
    errors: List[TemplateValidationError]

    @property
    def is_valid(self):
        return len(self.errors) == 0

    def to_json(self):
        return {
            "is_valid": self.is_valid,
            "errors": [e.to_json() for e in self.errors]
        }


def validate_campaign_template(template: Dict):
    validator = Draft7Validator(CAMPAIGN_SCHEMA)
    errors = sorted(validator.iter_errors(template), key=lambda e: e.path)
    if errors:
        raise ValidationError(errors)


def prepare_validation_report(template: Dict) -> TemplateValidationReport:
    errors = []
    try:
        validate_campaign_template(template)
    except ValidationError as exception:
        errors = [
            TemplateValidationError("template_error", e.message.message)
            for e in exception.error_list
        ]
    return TemplateValidationReport(errors=errors)
