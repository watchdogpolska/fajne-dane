from dataclasses import dataclass
from typing import List, Tuple, Text

import pandas as pd
from django.core.exceptions import ValidationError

from django.utils.translation import gettext_lazy as _
from campaigns.models import Campaign, Query
from campaigns.models.dto.document import DocumentDTO
from campaigns.models.dto.record import RecordDTO
from campaigns.parsers.base import Parser
from campaigns.validators.data_frame import DataFrameValidator
from campaigns.validators.parsing_report import ParsingReport, DocumentParsingReport
from campaigns.validators.report import ValidationError as ParsingError
from fajne_dane.core.utils import encoding


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
        errors = []

        # read data fields
        data = {}
        for field in self.campaign.document_fields_objects:
            value = first_row[('data_fields', field.name)]
            if pd.isnull(value):
                continue
            data[field.name] = encoding.decode_numpy(value)

        # read queries
        records = {}
        for query in self.campaign.queries_objects:
            records[query.name] = []
            try:
                for record in _parse_records(query, document_data):
                    records[query.name].append(record)
            except ValidationError as e:
                errors.append(e)
                continue

        if errors:
            raise ValidationError({"data": errors})

        return DocumentDTO(
            data=data,
            records=records
        )

    def _validate_data_frame(self, df: pd.DataFrame) -> List[ParsingError]:
        file_errors = []
        try:
            DataFrameValidator(campaign=self.campaign).validate(df)
        except ValidationError as e:
            file_errors = [
                ParsingError(
                    code=error.code,
                    message=error.message % error.params
                )
                for error in e.error_dict['data']
            ]
        return file_errors

    def _parse_documents(self, df: pd.DataFrame) -> Tuple[List[DocumentDTO], List[DocumentParsingReport]]:
        documents, documents_errors = [], []
        document_fields_columns = [
            ('data_fields', f.name)
            for f in self.campaign.document_fields.all()
        ]

        for _, document_rows in df.groupby(document_fields_columns, dropna=False):
            document_index, document_data = document_rows.index[0], None
            try:
                document = self._parse_document(document_rows)
                self.campaign.validate_document(document)
                documents.append(document)
            except ValidationError as e:
                documents_errors.append(
                    DocumentParsingReport(
                        index=document_index,
                        data=document.data,
                        errors=[
                            ParsingError(
                                code=error.code,
                                message=error.message % error.params
                            )
                            for error in e.error_dict['data']
                        ]
                    )
                )
        return documents, documents_errors

    def parse(self, df: pd.DataFrame) -> ParsingReport:
        file_errors = self._validate_data_frame(df)
        documents, documents_errors = [], []
        if not file_errors:
            documents, documents_errors = self._parse_documents(df)
        return ParsingReport(file_errors, documents, documents_errors)
