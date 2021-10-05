from dataclasses import dataclass
from typing import Any, Dict

from .base import Template
from ..type import validate_type


@dataclass
class DocumentDataFieldTemplate(Template):
    name: str
    widget: str
    type: str

    def validate(self, value: Any) -> bool:
        return validate_type(value, self.type)

    @staticmethod
    def from_json(data_field_template: Dict) -> "DocumentDataFieldTemplate":
        return DocumentDataFieldTemplate(
            name=data_field_template['name'],
            type=data_field_template['type'],
            widget=data_field_template['widget'],
        )
