from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.utils import timezone

from campaigns.models import Source, FileSource, Document
from campaigns.models.sources.source import SourceTypes
from campaigns.validators.parsing_report import ParsingReport
from tests.campaigns.conftest import basic_campaign, basic_campaign_with_queries, advanced_campaign_with_queries, \
    setup_institutions
from tests.conftest import basic_campaign_documents_file, wrong_advanced_campaign_documents_file


def fake_file() -> SimpleUploadedFile:
    with basic_campaign_documents_file(mode='rb') as f:
        return SimpleUploadedFile(
            "input.txt",
            f.read()
        )


def file_source_with_file() -> FileSource:
    source = FileSource.objects.create(
        name="file source",
        description="this is a file",
        campaign=basic_campaign_with_queries(),
        source_link="http://source.link",
        source_date=timezone.now(),
        file=fake_file()
    )
    return source


def wrong_fake_file() -> SimpleUploadedFile:
    with wrong_advanced_campaign_documents_file(mode='rb') as f:
        return SimpleUploadedFile(
            "wrong_input.txt",
            f.read()
        )


def file_source_with_wrong_file() -> FileSource:
    source = FileSource.objects.create(
        name="file source",
        description="this is a file",
        campaign=advanced_campaign_with_queries(),
        source_link="http://source.link",
        source_date=timezone.now(),
        file=wrong_fake_file()
    )
    return source


class FileSourceTestCase(TestCase):

    def test_creating(self):
        source = FileSource.objects.create(
            name="file source",
            description="this is a file",
            campaign=basic_campaign_with_queries(),
            source_link="http://source.link",
            source_date=timezone.now(),
            file=fake_file()
        )

        self.assertIsInstance(source, FileSource)
        self.assertIsInstance(source, Source)
        self.assertEqual(source.type, SourceTypes.FILE)

    def test_parse_file(self):
        source = file_source_with_file()

        report = source.parse_file()
        self.assertIsInstance(report, ParsingReport)
        self.assertEqual(report.is_valid, True)
        self.assertEqual(report.valid_documents_count, 4)
        self.assertEqual(report.invalid_documents_count, 0)
        self.assertEqual(len(report.documents_errors), 0)
        self.assertEqual(len(report.file_errors), 0)

    def test_parse_file_wrong(self):
        source = file_source_with_wrong_file()

        report = source.parse_file()
        self.assertIsInstance(report, ParsingReport)
        self.assertEqual(report.is_valid, False)
        self.assertEqual(report.valid_documents_count, 1)
        self.assertEqual(report.invalid_documents_count, 3)
        self.assertEqual(len(report.documents_errors), 3)
        self.assertEqual(len(report.file_errors), 0)

    def test_creating_documents(self):
        setup_institutions()
        source = file_source_with_file()
        report = source.parse_file()
        source.create_documents(report)

        self.assertEqual(Document.objects.count(), 4)
        self.assertEqual(source.campaign.documents.count(), 4)
