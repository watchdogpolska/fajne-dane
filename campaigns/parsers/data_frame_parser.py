from dataclasses import dataclass
from typing import List

import pandas as pd

from campaigns.models import Campaign, Query
from campaigns.models.dto.document import DocumentDTO
from campaigns.models.dto.record import RecordDTO
from campaigns.parsers.base import Parser


def _parse_records(query: Query, records_data: pd.DataFrame) -> List[RecordDTO]:
    field_name = query.output_field.name
    probability_name = field_name + "__probability"

    _records = records_data[[(query.name, field_name), (query.name, probability_name)]].dropna()
    _records.columns = _records.columns.get_level_values(1)
    records = _records.to_dict(orient='records')

    return [
        RecordDTO(
            value=record[field_name],
            probability=record[probability_name]
        )
        for record in records
    ]


@dataclass
class DataFrameParser(Parser):
    campaign: Campaign

    def _parse_document(self, document_data: pd.DataFrame) -> DocumentDTO:
        first_row = document_data.iloc[0]

        # read data fields
        data = {}
        for field in self.campaign.document_fields_objects:
            data[field.name] = first_row[('data_fields', field.name)]
        # read queries
        records = {}
        for query in self.campaign.queries_objects:
            for record in _parse_records(query, document_data):
                records[query.name] = record

        return DocumentDTO(
            data=data,
            records=records
        )


    def parse(self, df: pd.DataFrame) -> List[DocumentDTO]:
        document_fields_columns = [
            ('data_fields', f)
            for f in [
                f.name
                for f in self.campaign.document_fields.all()
            ]
        ]

        # parse documents
        documents = []
        for i, document_rows in df.groupby(document_fields_columns):
            document = self._parse_document(document_rows)
            self.campaign.validate_document(document)
            documents.append(document)
        return documents
