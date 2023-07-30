from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from campaigns.models import Campaign
from campaigns.validators.parsing_report import ParsingReport


@dataclass
class CampaignParser(ABC):
    campaign: Campaign

    @abstractmethod
    def parse(self, data: Any) -> ParsingReport:
        ...
