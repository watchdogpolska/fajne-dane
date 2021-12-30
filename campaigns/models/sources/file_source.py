from typing import List
from typing import TYPE_CHECKING

from django.db import models

from .source import Source, SourceTypes
from .utils import load_data_frame

if TYPE_CHECKING:
    from campaigns.models import Document

from campaigns.validators.parsing_report import ParsingReport

class FileSource(Source):
    campaign = models.ForeignKey("Campaign",
                                 on_delete=models.CASCADE,
                                 related_name="file_sources")
    description = models.TextField(default="", blank=True)
    file = models.FileField(upload_to='resources')  # uploads to S3

    def __init__(self, *args, **kwargs):
        if 'type' not in kwargs:
            kwargs['type'] = SourceTypes.FILE
        super().__init__(*args, **kwargs)

    def parse_file(self) -> ParsingReport:
        from campaigns.parsers.data_frame_parser import DataFrameParser
        df = load_data_frame(self.file)
        parser = DataFrameParser(campaign=self.campaign)
        report = parser.parse(df)
        return report

    def create_documents(self, report: ParsingReport) -> List["Document"]:
        from campaigns.models.factory.documents_factory import DocumentsFactory
        factory = DocumentsFactory(campaign=self.campaign, source=self)
        documents = factory.bulk_create(report.documents)
        return documents
