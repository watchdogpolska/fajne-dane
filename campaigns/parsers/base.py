from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from campaigns.validators.parsing_report import ParsingReport


@dataclass
class Parser(ABC):
    @abstractmethod
    def parse(self, data: Any) -> ParsingReport:
        ...
