from typing import Any

from django.core.exceptions import ValidationError
from jsonschema import Draft7Validator
from django.utils.translation import gettext_lazy as _


def validate_json_meta_schema(schema: dict):
    """
    Checks if the input is a valid JSON schema. In practice it checks if the provided
    schema is following format of JSON meta schema.

    :param schema: dict - a schema that will be validated
    :raises ValidationError
    """
    validator = Draft7Validator(Draft7Validator.META_SCHEMA)
    errors = sorted(validator.iter_errors(schema), key=lambda e: e.path)
    if errors:
        raise ValidationError(errors)
