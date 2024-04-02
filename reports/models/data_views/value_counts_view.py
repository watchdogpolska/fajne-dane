from typing import List

import pandas as pd
from django.db import models

from .data_view import DataView
from .consts import AggregationTypes, DataViewTypes


def _compute_values_counts(df: pd.DataFrame, values: List[str], threshold: int) -> pd.DataFrame:
    if len(values) == 1: values = values[0]
    _counts = df[values].value_counts()
    _df = _counts[_counts > threshold].to_frame("count")
    _df.loc['Inne'] = _counts[_counts <= threshold].sum()
    return _df.reset_index()


class ValueCountsView(DataView):
    threshold = models.IntegerField(default=0)

    def __init__(self, *args, **kwargs):
        if 'type' not in kwargs:
            kwargs['type'] = DataViewTypes.VALUE_COUNTS
            kwargs['aggregation'] = AggregationTypes.COUNT
        super().__init__(*args, **kwargs)

    def update(self):
        _df = _compute_values_counts(self.data_source.data, values=self.values, threshold=self.threshold)
        self._save_data(_df)
