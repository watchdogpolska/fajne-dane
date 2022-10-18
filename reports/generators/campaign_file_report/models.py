from dataclasses import dataclass
from typing import List, Text, Dict


@dataclass
class InstitutionData:
    group_id: int
    name: Text
    key: Text


@dataclass
class InstitutionGroupData:
    id: int
    name: Text
    depth: int


@dataclass
class QueryData:
    id: int
    value: Text


@dataclass
class DocumentReport:
    id: int
    institutions: List[InstitutionData]
    data: Dict[Text, Text]
    answers: Dict[int, List[Text]]


@dataclass
class Report:
    queries: Dict[int, QueryData]
    institutions_groups: Dict[int, InstitutionGroupData]
    documents: List[DocumentReport]
