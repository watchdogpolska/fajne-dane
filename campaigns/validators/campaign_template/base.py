from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class Template(ABC):

    @abstractmethod
    def validate(self, data: Any) -> bool:
        ...

    @staticmethod
    @abstractmethod
    def from_json(data: Dict) -> "Template":
        ...
