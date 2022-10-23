from collections import defaultdict
from typing import Any, Text, Dict, List

from io import BytesIO
from xlsxwriter.worksheet import Worksheet
from xlsxwriter.format import Format
from xlsxwriter import Workbook
from dataclasses import dataclass, field

from reports.generators.campaign_file_report.models import DocumentReport, Report
from reports.renderers.campaign_file_report.exceptions import NoWorksheetSet


def get_documents_data_fields(documents: List[DocumentReport]) -> List[Text]:
    fields = []
    for document in documents:
        for f in document.data.keys():
            if f not in fields:
                fields.append(f)
    return fields


@dataclass
class CampaignFileReportRenderer:
    report: Report
    _workbook: Workbook = field(init=False, default=None)
    _worksheet: Worksheet = field(init=False, default=None)
    _formats: Dict[Text, Format] = field(init=False, default_factory=dict)
    _columns_mapping: Dict[Text, Dict[Any, Any]] = field(init=False, default_factory=lambda: defaultdict(dict))

    def _setup_formats(self):
        text_format = self._workbook.add_format({
            'align': 'left',
            'valign': 'vcenter'
        })
        text_format.set_text_wrap()
        self._formats['text'] = text_format

        header_format = self._workbook.add_format({
            'align': 'center'
        })
        header_format.set_bold()
        self._formats['header'] = header_format

    def _write_value(self, row: int, column: int, value: Any, format_name: Text, rows: int=1, columns: int=1):
        if not self._worksheet:
            raise NoWorksheetSet()

        value_format = self._formats[format_name]
        if rows > 1 or columns > 1:
            self._worksheet.merge_range(row, column, row + rows - 1, column + columns - 1, value, value_format)
        else:
            self._worksheet.write(row, column, value, value_format)

    def _setup_header(self):
        offset = self._setup_documents_header(0)
        offset = self._setup_institutions_header(offset)
        self._setup_queries_header(offset)

    def _setup_documents_header(self, offset: int) -> int:
        column_index = offset
        document_data_fields = get_documents_data_fields(self.report.documents)

        self._write_value(0, column_index, "Dokument", 'header', columns=len(document_data_fields)+1)
        self._write_value(1, column_index, "Id", 'header')
        self._columns_mapping['document']['id'] = column_index
        column_index += 1

        for data_field in document_data_fields:
            self._write_value(1, column_index, data_field, 'header')
            self._columns_mapping['document'][data_field] = column_index
            column_index += 1

        return column_index

    def _setup_institutions_header(self, offset: int) -> int:
        column_index = offset
        for institution in sorted(self.report.institutions_groups.values(), key=lambda x: x.depth):
            self._write_value(0, column_index, institution.name, 'header', columns=2)
            self._write_value(1, column_index, "Klucz", 'header')
            self._write_value(1, column_index + 1, "Nazwa", 'header')
            self._columns_mapping['institution'][institution.id] = {
                'key': column_index,
                'name': column_index + 1
            }
            column_index += 2
        return column_index

    def _setup_queries_header(self, offset: int) -> int:
        column_index = offset
        for query in self.report.queries.values():
            self._write_value(0, column_index, f"Pytanie {query.order}", 'header')
            self._write_value(1, column_index, query.value, 'header')
            self._columns_mapping['query'][query.id] = column_index
            column_index += 1
        return column_index

    def _write_documents(self):
        row_offset = 2
        for document in self.report.documents:
            row_offset = self._write_document(document, row_offset)

    def _write_document(self, document: DocumentReport, offset: int):
        row_index = offset

        max_answers = 0
        for query_id, answers in document.answers.items():
            _mapping = self._columns_mapping['query'][query_id]
            max_answers = max(max_answers, len(answers))
            for index, answer in enumerate(answers):
                self._write_value(row_index + index, _mapping, answer, 'text')

        self._write_value(row_index, self._columns_mapping['document']['id'], document.id, 'text', rows=max_answers)

        for name, value in document.data.items():
            self._write_value(row_index, self._columns_mapping['document'][name], value, 'text', rows=max_answers)

        for institution in document.institutions:
            _mapping = self._columns_mapping['institution'][institution.group_id]
            self._write_value(row_index, _mapping['key'], institution.key, 'text', rows=max_answers)
            self._write_value(row_index, _mapping['name'], institution.name, 'text', rows=max_answers)

        row_index += max_answers
        return row_index

    def render(self) -> BytesIO:
        output = BytesIO()
        self._workbook = Workbook("shared/test.xlsx")
        self._worksheet = self._workbook.add_worksheet()
        self._setup_formats()
        self._setup_header()
        self._write_documents()
        self._workbook.close()
        return output
