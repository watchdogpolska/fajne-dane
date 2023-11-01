from functools import cache
from io import StringIO
from typing import List, Text

import pandas as pd
from django.core.files.base import ContentFile
from django.db import models
from django.db.models import QuerySet

from campaigns.models import Campaign, Record, Institution


def _get_campaign_institutions_data(campaign: Campaign) -> pd.DataFrame:
    institutions_data = {}
    for group_id in campaign.institution_groups_path:
        _institutions = Institution.objects.filter(group_id=group_id).values('id', 'key', 'name', 'parent')
        institutions_data[group_id] = {i['id']: i for i in _institutions}

    institution_groups_path = campaign.institution_groups_path
    data = []
    for institution in institutions_data[campaign.institution_group.id].values():
        _institution = institution
        row = {"institution_id": _institution['id']}
        for depth in range(len(institution_groups_path)):
            row[f"institution_key_{depth}"] = _institution['key']
            row[f"institution_name_{depth}"] = _institution['name']

            if depth + 1 < len(institution_groups_path):
                _parent_group = institution_groups_path[depth+1]
                _institution = institutions_data[_parent_group][_institution['parent']]
        data.append(row)

    return pd.DataFrame(data)


def _get_campaign_documents_data(source: "DataSource") -> pd.DataFrame:
    df_raw = pd.DataFrame(source.get_queryset())

    columns_mapping = {
        "parent__query": "query_id",
        "parent__document": "document_id"
    }

    # clean data columns
    data_columns = [c for c in df_raw.columns if c.startswith("parent__document__data")]
    for column in data_columns:
        columns_mapping[column] = column.replace("parent__document__data__", "data__")

    df_raw = df_raw.rename(columns=columns_mapping)

    value_columns = ["value", "query_id"]
    key_columns = list(set(df_raw.columns) - set(value_columns))

    data = []
    for key, group in df_raw.groupby(key_columns):
        key_data = group[key_columns].iloc[0].to_dict()
        answers_data = group[value_columns].set_index("query_id").T.iloc[0].to_dict()
        data.append({**key_data, **answers_data})

    df = pd.DataFrame(data)

    columns_mapping = {c: f"query_{c}__answer"  for c in df.columns if type(c) is int}
    df = df.rename(columns=columns_mapping)
    return df


def _get_campaign_report_data(source: "DataSource") -> pd.DataFrame:
    return pd.merge(
        _get_campaign_institutions_data(source.campaign),
        _get_campaign_documents_data(source),
        left_on='institution_id',
        right_on='parent__document__institution_id',
        how='left'
    )


class DataSource(models.Model):
    campaign = models.OneToOneField(Campaign, on_delete=models.CASCADE)
    file = models.FileField(upload_to='data_sources', null=True, blank=True)
    dirty = models.BooleanField(default=True)

    def mark(self):
        if not self.dirty:
            self.dirty = True
            self.save()

    @property
    def records(self) -> QuerySet:
        return Record.objects \
            .filter(
            status="ACCEPTED",
            parent__query__campaign=self.campaign)

    def _get_document_field(self) -> List[Text]:
        return [
            f"parent__document__data__{field.name}"
            for field in self.campaign.document_fields.all()
        ]

    def _get_value_fields(self) -> List[Text]:
        return ["value", "parent__query", "parent__document", "parent__document__institution_id"] +  \
            self._get_document_field()

    def get_queryset(self) -> QuerySet:
        return self.records.values(*self._get_value_fields())

    def update(self) -> None:
        _df = _get_campaign_report_data(self)
        output_file = ContentFile(_df.to_csv(index=False).encode('utf-8'))
        self.file.save(f"data_source_{self.id}.csv", output_file)
        self.dirty = False
        self.save()
        DataSource.data.fget.cache_clear()  # noqa

    def _load_data(self):
        _df = pd.read_csv(StringIO(self.file.read().decode('utf-8')))
        self.file.close()
        return _df

    @property
    @cache
    def data(self) -> pd.DataFrame:
        return self._load_data()
