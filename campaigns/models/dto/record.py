from dataclasses import dataclass
from typing import Any


@dataclass
class RecordDTO:
    value: Any
    probability: float
