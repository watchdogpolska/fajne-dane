from dataclasses import dataclass
from typing import List, Text


@dataclass
class InstitutionData:
    name: Text
    key: Text
    parent_id: int


@dataclass
class InstitutionGroupData:
    id: int
    name: Text


@dataclass
class InstitutionReport:
    data: List[InstitutionData]


@dataclass
class DocumentReport:
    id: int
    institution: InstitutionReport
    data: List[Text]
    answers: List[Text]

@dataclass
class Report:
    documents: List[DocumentReport]
