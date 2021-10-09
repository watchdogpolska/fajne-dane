from dataclasses import dataclass, field
from typing import Dict, Optional

from . import RecordDTO


@dataclass
class DocumentDTO:
    data: Dict
    records: Optional[Dict[str, RecordDTO]] = field(default_factory=dict)
