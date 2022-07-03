from dataclasses import dataclass, field
from typing import Text, Dict


@dataclass
class InstitutionDTO:
    key: Text
    name: Text
    metadata: Dict = field(default_factory=dict)
