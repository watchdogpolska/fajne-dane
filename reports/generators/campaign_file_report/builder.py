from collections import defaultdict
from dataclasses import dataclass, field
from functools import cache
from itertools import groupby
from typing import Iterable, List, Dict, Text, Any, Tuple

from campaigns.models import Query
from reports.aggregations.models.institution_paths import InstitutionGroupPaths
from reports.generators.campaign_file_report.models import Report, InstitutionData, DocumentReport, \
    InstitutionGroupData, QueryData
from reports.models import CampaignDataSource

document_key_func = lambda x: x['parent__document']
document_query_key_func = lambda x: x['parent__query']


def get_documents_institutions(group_data: Dict[Text, Any]) -> List[InstitutionData]:
    _data = defaultdict(dict)
    for key, value in group_data.items():
        if not key.startswith('parent__document__institution'):
            continue
        key_parts = key.split('__')
        index = "__".join(key_parts[:-1])
        field = key_parts[-1]
        if value:
            _data[index][field] = value

    return [
        InstitutionData(
            key=value['key'],
            name=value['name'],
            group_id=value['group']
        )
        for value in _data.values()
    ]


def get_document_data(group_data: Dict[str, Any]) -> Dict[Text, Text]:
    return {
        key.split('__')[-1]: value
        for key, value in group_data.items()
        if key.startswith('parent__document__data')
    }


def get_document_answers(group_data: List[Dict[Text, Any]]) -> Dict[int, List[Text]]:
    document_answers = defaultdict(list)
    for query_id, query_data in groupby(group_data, key=document_query_key_func):
        for record in query_data:
            document_answers[query_id].append(record['value'])
    return document_answers


def get_institutions_groups_data(institution_group_paths: InstitutionGroupPaths) -> Dict[int, InstitutionGroupData]:
    return {
        group.id: InstitutionGroupData(
            id=group.id,
            name=group.name,
            depth=institution_group_paths.depth[group.id]
        )
        for group in institution_group_paths.mapping.values()
    }


def get_queries_data(queries: List[Query]) -> Dict[int, QueryData]:
    return {
        q.id: QueryData(
            id=q.id,
            value=q.data[q.main_question_index]
        )
        for q in queries
    }


@dataclass
class FileReportBuilder:
    file_report: "FileReport"
    _queries_mapping: Dict[int, Query] = field(init=False, default_factory=dict)

    @property
    def data_source(self) -> CampaignDataSource:
        return self.file_report.data_source

    @property
    def documents_groups(self) -> Iterable[Tuple[int, Iterable[Dict[Text, Any]]]]:
        return groupby(
            sorted(
                list(self.data_source.get_queryset()),
                key=document_key_func
            ),
            key=document_key_func
        )

    @property
    def queries_mapping(self):
        if not self._queries_mapping:
            self._queries_mapping = {
                q.id: q
                for q in Query.objects.filter(campaign=self.data_source.campaign)
            }
        return self._queries_mapping

    def generate(self) -> Report:
        institutions_groups_data = get_institutions_groups_data(self.data_source.institution_group_paths)
        queries_data = get_queries_data(list(self.queries_mapping.values()))

        documents_reports = []
        for document_id, group_data in self.documents_groups:
            group_data = list(group_data)
            # gather values for each query
            document_institutions = get_documents_institutions(group_data[0])
            document_data = get_document_data(group_data[0])
            document_answers = get_document_answers(group_data)

            documents_reports.append(
                DocumentReport(
                    id=document_id,
                    institutions=document_institutions,
                    data=document_data,
                    answers=document_answers
                )
            )
        return Report(
            institutions_groups=institutions_groups_data,
            queries=queries_data,
            documents=documents_reports
        )
