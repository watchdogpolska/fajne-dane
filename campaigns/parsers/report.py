from dataclasses import dataclass
from typing import List, Dict

from campaigns.models.dto import DocumentDTO


@dataclass
class ParsingError:
    code: str
    message: str


@dataclass
class DocumentError:
    index: int
    data: Dict
    errors: List[ParsingError]


@dataclass
class ParsingReport:
    documents: List[DocumentDTO]
    errors: List[DocumentError]

    @property
    def is_valid(self):
        return len(self.errors) == 0
