from dataclasses import field, dataclass
from typing import List, Dict, Any

from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from .base import Template
from ..type import validate_type
from ...models.dto.record import RecordDTO


@dataclass
class OutputFieldTemplate(Template):
    name: str
    type: str
    validation: bool
    answers: List[Any] = field(default=None)

    def validate(self, record: RecordDTO):
        errors = []
        try:
            validate_type(record.value, self.type)
        except ValidationError as e:
            errors.append(e)

        if self.answers:
            if self.validation and record.value not in self.answers:
                errors.append(
                    ValidationError(
                        _("Record value: %(value)s not found in the list of accepted answers."),
                        code='invalid-value',
                        params={'value': record.value}
                    )
                )
        if errors:
            raise ValidationError(errors)

    @staticmethod
    def from_json(output_field_template: Dict) -> "OutputFieldTemplate":
        return OutputFieldTemplate(
            name=output_field_template['name'],
            type=output_field_template['type'],
            answers=output_field_template.get('answers'),
            validation=output_field_template.get('validation')
        )
