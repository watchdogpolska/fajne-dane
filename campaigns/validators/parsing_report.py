from dataclasses import dataclass
from typing import List, Dict

from campaigns.models.dto import DocumentDTO
from campaigns.validators.report import ValidationReport


@dataclass
class DocumentParsingReport(ValidationReport):
    index: int
    data: Dict

    def to_json(self):
        return {
            "index": self.index,
            "data": self.data,
            **self.to_json()
        }


@dataclass
class ParsingReport:
    documents: List[DocumentDTO]
    errors: List[DocumentParsingReport]

    @property
    def is_valid(self):
        return len(self.errors) == 0

    @property
    def valid_documents_count(self):
        return len(self.documents)

    @property
    def invalid_documents_count(self):
        return len(self.errors)

    def to_json(self):
        return {
            "is_valid": self.is_valid,
            "valid_documents_count": self.valid_documents_count,
            "invalid_documents_count": self.invalid_documents_count,
            "errors": [e.to_json() for e in self.errors]
        }
