from typing import List

import pandas as pd

from campaigns.models.dto.document import DocumentDTO
from campaigns.models.dto.record import RecordDTO
from campaigns.parsers.base import Parser
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


class DataFrameParser(Parser):
    def parse(self, df: pd.DataFrame) -> List[DocumentDTO]:
        template = self.campaign.campaign_template
        document_fields = [f.name for f in template.document_schema.data_field_schemas]
        document_fields_columns = [('data_fields', f) for f in document_fields]

        # parse documents
        documents = []
        for i, document_rows in df.groupby(document_fields_columns):
            document = _parse_document(template, document_rows)
            template.validate(document)
            documents.append(document)

        return documents
