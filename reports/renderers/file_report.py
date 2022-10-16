import pandas as pd
from dataclasses import dataclass, field


@dataclass
class FileReportRenderer:
    report: pd.DataFrame

    def render(self):
        ...
