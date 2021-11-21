from dataclasses import dataclass, field
from typing import Dict, Optional, List

from . import RecordDTO


@dataclass
class DocumentDTO:
    data: Dict
    records: Optional[Dict[str, List[RecordDTO]]] = field(default_factory=dict)
