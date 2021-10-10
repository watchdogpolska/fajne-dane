from typing import Any

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

TYPES_MAPPING = {
    "int": int,
    "str": str,
    "float": float
}


def validate_type(value: Any, type_name: str):
    try:
        _type = TYPES_MAPPING[type_name]
        _type(value)
    except ValueError:
        raise ValidationError(
            _("Value type is not matching expected type: '%(type_name)s'."),
            code='wrong-type',
            params={'type_name': type_name}
        )
