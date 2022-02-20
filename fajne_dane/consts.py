from enum import Enum
from typing import Text

from fajne_dane.settings import API_URL, PANEL_URL


class Platform(Enum):
    API = "api"
    PANEL = "panel"
