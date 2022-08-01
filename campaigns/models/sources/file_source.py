from typing import List
from typing import TYPE_CHECKING

from django.db import models

from .source import Source, SourceTypes
from .utils import load_data_frame

if TYPE_CHECKING:
    from campaigns.models import Document

from campaigns.validators.parsing_report import ParsingReport


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


class FileSource(Source):
    campaign = models.ForeignKey("Campaign",
                                 on_delete=models.CASCADE,
                                 related_name="file_sources")
    source_link = models.URLField(default="", blank=True)
    source_date = models.DateTimeField()
    description = models.TextField(default="", blank=True)
    created = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='resources')  # uploads to S3

    def __init__(self, *args, **kwargs):
        if 'type' not in kwargs:
            kwargs['type'] = SourceTypes.FILE
        super().__init__(*args, **kwargs)

    def parse_file(self) -> ParsingReport:
        from campaigns.parsers.campaign_dataset_parser import CampaignDatasetParser
        df = load_data_frame(self.file)
        parser = CampaignDatasetParser(campaign=self.campaign)
        report = parser.parse(df)
        return report

    def create_documents(self, report: ParsingReport, batch_size: int = 100) -> List["Document"]:
        from campaigns.models.factory.documents_factory import DocumentsFactory
        factory = DocumentsFactory(campaign=self.campaign, source=self)
        for chunk in chunks(report.documents, batch_size):
            print("processing chunk")
            factory.bulk_create(chunk)
