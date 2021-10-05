from dataclasses import dataclass
from typing import List, Dict

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .base import Template
from .document_data_field_template import DocumentDataFieldTemplate
from ...models.dto.document import DocumentDTO


@dataclass
class DocumentTemplate(Template):
    data_field_templates: List[DocumentDataFieldTemplate]

    def validate(self, document: DocumentDTO):
        self.validate_data(document.data)

    def validate_data(self, data: Dict):
        errors = []
        for field_template in self.data_field_templates:
            try:
                value = data[field_template.name]
                field_template.validate(value)
            except KeyError:
                errors.append(
                    ValidationError(
                        _("Field: %(value)s not found in the document data."),
                        code='missing-field',
                        params={'value': field_template.name}
                    )
                )
            except ValidationError as e:
                errors.append(e)

        if errors:
            raise ValidationError(errors)

    @staticmethod
    def from_json(document_template: Dict) -> "DocumentTemplate":
        return DocumentTemplate(
            data_field_templates=[
                DocumentDataFieldTemplate.from_json(d)
                for d in document_template['data_fields']
            ]
        )
