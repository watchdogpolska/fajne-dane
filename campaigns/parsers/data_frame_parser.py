from dataclasses import dataclass
from typing import List

import pandas as pd

from campaigns.models import Campaign
from campaigns.parsers.base import Parser
from campaigns.models.dto.document import DocumentDTO
from campaigns.models.dto.record import RecordDTO
from campaigns.validators.campaign_template import CampaignTemplate
from campaigns.validators.campaign_template.query_template import QueryTemplate


def _parse_document(schema: CampaignTemplate, document_data: pd.DataFrame) -> DocumentDTO:
    first_row = document_data.iloc[0]

    # read data fields
    data = {}
    for field in schema.document_schema.data_field_schemas:
        data[field.name] = first_row[('data_fields', field.name)]

    # read queries
    records = {}
    for query in schema.query_schemas:
        for record in _parse_records(query, document_data):
            records[query.name] = record

    return DocumentDTO(
        data=data,
        records=records
    )


def _parse_records(query: QueryTemplate, records_data: pd.DataFrame) -> List[RecordDTO]:
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

    def parse(self, df: pd.DataFrame) -> List[DocumentDTO]:
        document_fields_columns = [
            ('data_fields', f)
            for f in [
                f.name
                for f in self.campaign.document_fields.all()
            ]
        ]
        print(document_fields_columns)

        # parse documents
        documents = []
        for i, document_rows in df.groupby(document_fields_columns):
            document = _parse_document(template, document_rows)
            break
            template.validate(document)
            documents.append(document)
        3/0

        return documents
