import json

from django.core.exceptions import ValidationError
from jsonschema import Draft7Validator

from campaigns.validators.utils import validate_json_meta_schema
from pathlib import Path

CAMPAIGN_SCHEMA = json.load(open(Path(__file__).resolve().parent / "./schemas/campaign_template-schema.json"))
validate_json_meta_schema(CAMPAIGN_SCHEMA)


def validate_campaign_template(template: dict):
    validator = Draft7Validator(CAMPAIGN_SCHEMA)
    errors = sorted(validator.iter_errors(template), key=lambda e: e.path)
    if errors:
        raise ValidationError(errors)
