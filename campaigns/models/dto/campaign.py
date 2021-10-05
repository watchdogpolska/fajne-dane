from dataclasses import dataclass
from typing import Dict

from .query import QueryDTO


@dataclass
class CampaignDTO:
    queries: Dict[str, QueryDTO]