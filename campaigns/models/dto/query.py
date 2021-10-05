from dataclasses import dataclass
from typing import Dict

from .output_field import OutputFieldDTO


@dataclass
class QueryDTO:
    order: int
    name: str
    data: Dict
    output_field = OutputFieldDTO
