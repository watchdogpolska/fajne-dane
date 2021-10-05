from dataclasses import dataclass
from typing import List, Dict

from campaigns.models.dto import DocumentDTO
from .base import Template
from .document_template import DocumentTemplate
from .query_template import QueryTemplate


@dataclass
class CampaignTemplate(Template):
    document_template: DocumentTemplate
    query_schemas: List[QueryTemplate]

    def validate(self, document: DocumentDTO):
        self.document_template.validate(document)

        for query_schema in self.query_schemas:
            record = document.records.get(query_schema.name)
            if not record:
                continue
            query_schema.validate(record)

    @staticmethod
    def from_json(campaign_template: Dict) -> "CampaignTemplate":
        return CampaignTemplate(
            document_template=DocumentTemplate.from_json(campaign_template['document']),
            query_schemas=[
                QueryTemplate.from_json(q)
                for q in campaign_template['queries']
            ]
        )
