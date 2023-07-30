from typing import List, Tuple
from typing import TYPE_CHECKING

from django.db import models, transaction
from django.db.transaction import atomic

from .source import Source, SourceTypes
from .utils import load_data_frame
from ..consts import FileSourceStatus
from ..dto import DocumentDTO

if TYPE_CHECKING:
    from campaigns.models import Document

from campaigns.validators.parsing_report import ParsingReport, ParsingValidationReport


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
    status = models.CharField(max_length=12,
                              choices=FileSourceStatus.choices,
                              default=FileSourceStatus.CREATED)
    raw_report = models.JSONField(default=dict)

    def __init__(self, *args, **kwargs):
        if 'type' not in kwargs:
            kwargs['type'] = SourceTypes.FILE
        super().__init__(*args, **kwargs)

    def validate_file(self) -> ParsingValidationReport:
        from campaigns.parsers.campaign_dataset_parser import CampaignDatasetParser
        df = load_data_frame(self.file)
        parser = CampaignDatasetParser(campaign=self.campaign)
        return parser.validate(df)

    def parse_file(self) -> Tuple[ParsingReport, List[DocumentDTO]]:
        from campaigns.parsers.campaign_dataset_parser import CampaignDatasetParser
        df = load_data_frame(self.file)
        parser = CampaignDatasetParser(campaign=self.campaign)
        return parser.parse(df)


    @transaction.atomic()
    def create_documents(self, documents: List[DocumentDTO], batch_size: int = 100) -> List["Document"]:
        from campaigns.models.factory.documents_factory import DocumentsFactory
        factory = DocumentsFactory(campaign=self.campaign, source=self)
        for chunk in chunks(documents, batch_size):
            factory.bulk_create(chunk)

    def process(self):
        self.update_status(FileSourceStatus.PROCESSING)

        report, documents = self.parse_file()
        self.raw_report = report.to_json()
        self.save()

        if report.is_valid:
            self.create_documents(documents)
            new_status = FileSourceStatus.FINISHED
        else:
            new_status = FileSourceStatus.FAILED

        self.update_status(new_status)

    def update_status(self, status: FileSourceStatus, save: bool = True):
        self.status = status
        if save:
            self.save()

    @property
    def report(self) -> ParsingReport:
        return ParsingReport.from_json(self.raw_report)
