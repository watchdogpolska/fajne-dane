from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class OutputFieldDTO:
    name: str
    widget: str
    answers: List[Any]
    meta: Dict
    type: str
    validation: bool
    default_answer: Any
