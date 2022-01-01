from dataclasses import dataclass
from typing import List, Dict

from campaigns.models.dto import DocumentDTO
from campaigns.validators.report import ValidationReport, ValidationError as FileParsingError


@dataclass
class DocumentParsingReport(ValidationReport):
    index: int
    data: Dict

    def to_json(self):
        return {
            "index": self.index,
            "data": self.data,
            **super().to_json()
        }


@dataclass
class ParsingReport:
    file_errors: List[FileParsingError]
    documents: List[DocumentDTO]
    documents_errors: List[DocumentParsingReport]

    @property
    def is_valid(self):
        return len(self.file_errors) == 0 and self.invalid_documents_count == 0

    @property
    def valid_documents_count(self):
        return len(self.documents)

    @property
    def invalid_documents_count(self):
        return len(self.documents_errors)

    def to_json(self):
        return {
            "is_valid": self.is_valid,
            "valid_documents_count": self.valid_documents_count,
            "invalid_documents_count": self.invalid_documents_count,
            "documents_errors": [e.to_json() for e in self.documents_errors],
            "file_errors": [e.to_json() for e in self.file_errors]
        }
