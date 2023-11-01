from dataclasses import dataclass
from typing import List, Dict

from campaigns.models.dto import DocumentDTO
from campaigns.validators.report import ValidationReport, ValidationError as FileParsingError, ValidationError


@dataclass
class DocumentParsingReport(ValidationReport):
    index: int
    data: Dict

    def to_json(self):
        return {
            "index": int(self.index),
            "data": self.data,
            **super().to_json()
        }

    @staticmethod
    def from_json(data: dict) -> "DocumentParsingReport":
        return DocumentParsingReport(
            index=data["index"],
            data=data["data"],
            errors=[
                ValidationError.from_json(error_data)
                for error_data in data["errors"]
            ]
        )


@dataclass
class ParsingValidationReport:
    file_errors: List[FileParsingError]

    @property
    def is_valid(self):
        return len(self.file_errors) == 0

    def to_json(self):
        return {
            "is_valid": self.is_valid,
            "file_errors": [e.to_json() for e in self.file_errors]
        }

    @staticmethod
    def from_json(data: dict) -> "ParsingValidationReport":
        return ParsingValidationReport(
            file_errors=[
                FileParsingError.from_json(error_data)
                for error_data in data["file_errors"]
            ]
        )

@dataclass
class ParsingReport(ParsingValidationReport):
    valid_documents_count: int
    documents_errors: List[DocumentParsingReport]

    @property
    def is_valid(self):
        return super().is_valid and self.invalid_documents_count == 0

    @property
    def invalid_documents_count(self):
        return len(self.documents_errors)

    def to_json(self):
        return {
            **super().to_json(),
            **{
                "valid_documents_count": self.valid_documents_count,
                "invalid_documents_count": self.invalid_documents_count,
                "documents_errors": [e.to_json() for e in self.documents_errors],
            }
        }

    @staticmethod
    def from_json(data: dict) -> "ParsingReport":
        return ParsingReport(
            valid_documents_count=data["valid_documents_count"],
            documents_errors=[
                DocumentParsingReport.from_json(error_data)
                for error_data in data["documents_errors"]
            ],
            file_errors=[
                ValidationError.from_json(error_data)
                for error_data in data["file_errors"]
            ],
        )
