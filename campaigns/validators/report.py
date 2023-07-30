from dataclasses import dataclass
from typing import List


@dataclass
class ValidationError:
    code: str
    message: str

    def to_json(self):
        return { "code": self.code, "message": self.message }

    @staticmethod
    def from_json(data: dict) -> "ValidationError":
        return ValidationError(
            code=data["code"],
            message=data["message"]
        )


@dataclass
class ValidationReport:
    errors: List[ValidationError]

    @property
    def is_valid(self):
        return len(self.errors) == 0

    def to_json(self):
        return {
            "is_valid": self.is_valid,
            "errors": [e.to_json() for e in self.errors]
        }

    @staticmethod
    def from_json(data: dict) -> "ValidationReport":
        return ValidationReport(
            errors=[
                ValidationError.from_json(error_data)
                for error_data in data["errors"]
            ]
        )
