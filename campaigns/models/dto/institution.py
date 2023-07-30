from dataclasses import dataclass, field
from typing import Text, Dict, Optional


@dataclass
class InstitutionDTO:
    id: Optional[int] = None
    key: Optional[Text] = None
    name: Optional[Text] = None
    metadata: Dict = field(default_factory=dict)
