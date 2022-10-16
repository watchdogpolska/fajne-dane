from dataclasses import dataclass
from dataclasses import dataclass
from functools import cache
from itertools import groupby
from typing import Iterable, List, Dict, Text, Any, Tuple

from campaigns.models import Query
from reports.generators.campaign_file_report.models import Report
from reports.models import CampaignDataSource

document_key_func = lambda x: x['parent__document']
document_query_key_func = lambda x: x['parent__query']




@dataclass
class FileReportBuilder:
    file_report: "FileReport"

    @property
    def data_source(self) -> CampaignDataSource:
        return self.file_report.data_source

    @property
    def documents_groups(self) -> Iterable[Tuple[int, Iterable[List[Dict[Text, Any]]]]]:
        return groupby(
            sorted(
                list(self.data_source.get_queryset()),
                key=document_key_func
            ),
            key=document_key_func
        )

    @property
    @cache
    def queries_mapping(self):
        return { q.id: q for q in Query.objects.filter(campaign=self.data_source.campaign) }

    def generate(self) -> Report:
        documents_reports = []
"""

        for document_id, group_data in self.documents_groups:
            group_data = list(group_data)
            row = defaultdict(list)
            # gather values for each query

            for query_id, query_data in groupby(group_data, key=document_query_key_func):
                query = self.queries_mapping[query_id]
                query_value = query.data[0]['value']
                query_data = list(query_data)

                for record in query_data:
                    row[query_value].append(record['value'])
                max_records_count = max(len(row[query_value]), max_records_count)

            row_df = pd.DataFrame(row)
            row_df.columns = pd.MultiIndex.from_tuples([("Odpowiedzi", c) for c in row_df.columns])

            _first = group_data[0]
            row_df[("Instytucja", "nazwa")] = _first['parent__document__institution__name']
            row_df[("Instytucja", "klucz")] = _first['parent__document__institution__key']
            row_df[("Dokument", "url")] = _first['parent__document__data__document_url']
            row_df[("Dokument", "id")] = document_id

            institutions = []



            documents_reports.append(
                DocumentReport(
                )
            )
            ...
        return Report(documents_reports)


@dataclass
class FileReportBuilderBack:
    file_report: "FileReport"

    def generate(self) -> pd.DataFrame:
        ds = self.file_report.data_source

        raw_data = sorted(list(ds.get_queryset()), key=document_key_func)
        documents_raw_data = groupby(raw_data, key=document_key_func)

        queries = {
            q.id: q
            for q in Query.objects.filter(campaign=ds.campaign)
        }

        report_df = pd.DataFrame()

        for document_id, group_data in documents_raw_data:
            group_data = list(group_data)
            row = defaultdict(list)
            max_records_count = 0
            # gather values for each query
            for query_id, query_data in groupby(group_data, key=lambda x: x['parent__query']):
                query = queries[query_id]
                query_value = f"Pytanie {query.order} - {query.data[0]['value']}"
                query_data = list(query_data)

                for record in query_data:
                    row[query_value].append(record['value'])
                max_records_count = max(len(row[query_value]), max_records_count)

            for key, values in row.items():  # pad rows
                row[key] = values + [None] * (max_records_count - len(values))

            row_df = pd.DataFrame(row)
            row_df.columns = pd.MultiIndex.from_tuples([("Odpowiedzi", c) for c in row_df.columns])

            _first = group_data[0]
            row_df[("Instytucja", "nazwa")] = _first['parent__document__institution__name']
            row_df[("Instytucja", "klucz")] = _first['parent__document__institution__key']
            row_df[("Dokument", "url")] = _first['parent__document__data__document_url']
            row_df[("Dokument", "id")] = document_id

            report_df = pd.concat([report_df, row_df])
        return report_df

"""
