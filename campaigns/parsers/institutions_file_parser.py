from typing import Dict

import pandas as pd
from campaigns.models.dto import InstitutionDTO


def _parse_row(row: Dict) -> InstitutionDTO:
    return InstitutionDTO(
        key=row['key'],
        name=row['name'],
        metadata={
            key: value
            for key, value in row.items()
            if value and key not in ['key', 'name']
        }
    )


def parse(df: pd.DataFrame):
    # TODO: Dodać obsługę błędów i generować raport
    results = []
    df = df.fillna("")
    for row in df.to_dict(orient='records'):
        results.append(_parse_row(row))
    return results
