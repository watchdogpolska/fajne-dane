from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Any

from campaigns.models import Campaign


@dataclass
class Parser(ABC):
    campaign: Campaign

    @abstractmethod
    def parse(self, data: Any) -> Dict:
        ...
