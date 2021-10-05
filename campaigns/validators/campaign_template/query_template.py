from dataclasses import dataclass
from typing import Dict

from .base import Template
from .output_field_template import OutputFieldTemplate
from campaigns.models.dto import RecordDTO


@dataclass
class QueryTemplate(Template):
    name: str
    output_field_template: OutputFieldTemplate

    def validate(self, record_dto: RecordDTO):
        self.output_field_template.validate(record_dto)

    @staticmethod
    def from_json(query_template: Dict) -> "QueryTemplate":
        return QueryTemplate(
            name=query_template['name'],
            output_field_template=OutputFieldTemplate.from_json(query_template['output_field'])
        )
