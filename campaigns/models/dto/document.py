from dataclasses import dataclass
from typing import Dict

from . import RecordDTO


@dataclass
class DocumentDTO:
    data: Dict
    records: Dict[str, RecordDTO]
