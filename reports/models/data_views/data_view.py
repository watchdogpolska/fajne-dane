from functools import cache
from io import StringIO
from typing import List

import pandas as pd
from django.core.files.base import ContentFile
from django.db import models
from django.contrib.postgres.fields import ArrayField
from .consts import DataViewTypes, AggregationTypes

from .exceptions import DataViewError


def _compute_mean(df: pd.DataFrame, keys: List[str], values: List[str]) -> pd.DataFrame:
    return df.groupby(keys)[values].mean().reset_index()


def _compute_sum(df: pd.DataFrame, keys: List[str], values: List[str]) -> pd.DataFrame:
    return df.groupby(keys)[values].sum().reset_index()


def _compute_not_nan(df: pd.DataFrame, keys: List[str], values: List[str]) -> pd.DataFrame:
    df = df.copy()
    df[values] = df[values].notna()
    return df.groupby(keys)[values].mean().reset_index()


class DataView(models.Model):
    name = models.CharField(max_length=30)

    type = models.CharField(max_length=12,
                            choices=DataViewTypes.choices,
                            default=DataViewTypes.BASE)

    # used to do group-by aggregation
    keys = ArrayField(models.CharField(max_length=30), blank=True)
    values = ArrayField(models.CharField(max_length=30), blank=True)
    aggregation = models.CharField(max_length=30,
                                   choices=AggregationTypes.choices)

    # source of the data
    data_source = models.ForeignKey("DataSource",
                                    on_delete=models.CASCADE,
                                    related_name="views")

    # used to cache data saved as a csv file
    file = models.FileField(upload_to='data_views', null=True, blank=True)

    def to_child(self) -> "DataView":
        """
        Used to get an object of a child type object.
        """
        import reports.models.data_views as v
        if self.type == DataViewTypes.BASE:
            return v.data_view.DataView.objects.get(id=self.id)
        if self.type == DataViewTypes.VALUE_COUNTS:
            return v.value_counts_view.ValueCountsView.objects.get(id=self.id)
        raise TypeError(f"No child mapping found for type: {self.type}")

    def update(self):
        _df = None
        if self.aggregation == AggregationTypes.COUNT:
            raise DataViewError("Aggregation for this type shouldn't be done using base class.")
        elif self.aggregation == AggregationTypes.NOTNAN:
            _df = _compute_not_nan(self.data_source.data, keys=self.keys, values=self.values)
        elif self.aggregation == AggregationTypes.AVG:
            _df = _compute_mean(self.data_source.data, keys=self.keys, values=self.values)
        elif self.aggregation == AggregationTypes.SUM:
            _df = _compute_sum(self.data_source.data, keys=self.keys, values=self.values)
        self._save_data(_df)

    def _save_data(self, df: pd.DataFrame):
        output_file = ContentFile(df.to_csv(index=False).encode('utf-8'))
        self.file.save(f"data_source_{self.id}.csv", output_file)
        self.dirty = False
        self.save()
        DataView.data.fget.cache_clear()  # noqa

    def _load_data(self):
        _df = pd.read_csv(StringIO(self.file.read().decode('utf-8')))
        self.file.close()
        return _df

    @property
    def values_labels(self):
        return {
            value: self.data_source.query_labels[value]
            for value in self.values
        }

    @property
    @cache
    def data(self) -> pd.DataFrame:
        return self._load_data()
