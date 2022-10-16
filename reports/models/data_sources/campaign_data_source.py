from functools import cache
from typing import List, Text

from django.db import models
from django.db.models import QuerySet

from campaigns.models import Campaign, Record
from .data_source import DataSource, DataSourceTypes
from ...aggregations.models.institution_paths import (
    InstitutionGroupPaths, create_institution_group_paths
)


def _get_institution_fields(max_length: int) -> List[Text]:
    core_parts = [
        "".join(['parent__'] * index)
        for index in range(max_length)
    ]

    fields = []
    for core in core_parts:
        fields.append(f'parent__document__institution__{core}group')
        fields.append(f'parent__document__institution__{core}key')
        fields.append(f'parent__document__institution__{core}name')
    return fields



class CampaignDataSource(DataSource):
    campaign = models.OneToOneField(Campaign, on_delete=models.CASCADE)

    def __init__(self, *args, **kwargs):
        if 'type' not in kwargs:
            kwargs['type'] = DataSourceTypes.CAMPAIGN
        super().__init__(*args, **kwargs)


    @property
    def records(self) -> QuerySet:
        return Record.objects \
            .filter(
            status="ACCEPTED",
            parent__query__campaign=self.campaign)

    @property
    @cache
    def institution_group_paths(self) -> InstitutionGroupPaths:
        groups_ids = self.records.values_list(
            'parent__document__institution__group', flat=True).distinct()
        return create_institution_group_paths(groups_ids)

    def _get_institution_fields(self):
        return _get_institution_fields(self.institution_group_paths.max_length)

    def _get_document_field(self) -> List[Text]:
        # można zmienić to tak, żeby wybierać tylko niektóre pola
        # parent__document__institution
        return [
            f"parent__document__data__{field.name}"
            for field in self.campaign.document_fields.all()
        ]

    def _get_value_fields(self) -> List[Text]:
        return ["value", "parent__query", "parent__document"] +  \
            self._get_document_field() +  \
            self._get_institution_fields()

    def get_queryset(self) -> QuerySet:
        return self.records.values(*self._get_value_fields())
