from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class Parser(ABC):
    @abstractmethod
    def parse(self, data: Any) -> Any:
        ...
