
import json
from pathlib import Path
from typing import Dict

from django.core.exceptions import ValidationError
from jsonschema import Draft7Validator

from fajne_dane.core.utils.validators import validate_json_meta_schema


CAMPAIGN_SCHEMA = json.load(open(Path(__file__).resolve().parent / "./schemas/report_layout-schema.json"))
validate_json_meta_schema(CAMPAIGN_SCHEMA)


def validate_report_layout(template: Dict):
    validator = Draft7Validator(CAMPAIGN_SCHEMA)
    if errors := sorted(validator.iter_errors(template), key=lambda e: e.path):
        raise ValidationError(errors)

