from unittest.mock import MagicMock

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.utils import timezone

from campaigns.models import Source, FileSource, Document
from campaigns.models.consts import FileSourceStatus
from campaigns.models.sources.source import SourceTypes
from campaigns.validators.parsing_report import ParsingReport, ParsingValidationReport
from tests.campaigns.conftest import basic_campaign_with_queries, advanced_campaign_with_queries, \
    setup_institutions, file_source_with_file, wrong_data_fake_file, fake_file
from tests.conftest import wrong_advanced_campaign_documents_file, \
    wrong_schema_advanced_campaign_documents_file


def wrong_schema_fake_file() -> SimpleUploadedFile:
    with wrong_schema_advanced_campaign_documents_file(mode='rb') as f:
        return SimpleUploadedFile(
            "wrong_input.txt",
            f.read()
        )


def file_source_with_wrong_data_file() -> FileSource:
    return FileSource.objects.create(
        name="file source",
        description="this is a file",
        campaign=advanced_campaign_with_queries(),
        source_link="http://source.link",
        source_date=timezone.now(),
        file=wrong_data_fake_file(),
    )


def file_source_with_wrong_schema_file() -> FileSource:
    return FileSource.objects.create(
        name="file source",
        description="this is a file",
        campaign=advanced_campaign_with_queries(),
        source_link="http://source.link",
        source_date=timezone.now(),
        file=wrong_schema_fake_file(),
    )


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

        report, documents = source.parse_file()
        self.assertIsInstance(report, ParsingReport)
        self.assertEqual(report.is_valid, True)
        self.assertEqual(report.valid_documents_count, 4)
        self.assertEqual(report.invalid_documents_count, 0)
        self.assertEqual(len(report.documents_errors), 0)
        self.assertEqual(len(report.file_errors), 0)
        self.assertEqual(len(documents), 4)

    def test_validate_file_wrong_schema(self):
        source = file_source_with_wrong_schema_file()

        report = source.validate_file()
        self.assertIsInstance(report, ParsingValidationReport)
        self.assertEqual(report.is_valid, False)
        self.assertEqual(len(report.file_errors), 1)

    def test_parse_file_wrong_data(self):
        source = file_source_with_wrong_data_file()

        report, documents = source.parse_file()
        self.assertIsInstance(report, ParsingReport)
        self.assertEqual(report.is_valid, False)
        self.assertEqual(report.valid_documents_count, 1)
        self.assertEqual(report.invalid_documents_count, 3)
        self.assertEqual(len(report.documents_errors), 3)
        self.assertEqual(len(report.file_errors), 0)
        self.assertEqual(len(documents), 1)

    def test_creating_documents(self):
        setup_institutions()
        source = file_source_with_file()
        report, documents = source.parse_file()
        source.create_documents(documents)

        self.assertEqual(Document.objects.count(), 4)
        self.assertEqual(source.campaign.documents.count(), 4)

    def test_processing(self):
        setup_institutions()
        source = file_source_with_file()
        source.process()

        source.refresh_from_db()
        self.assertEqual(Document.objects.count(), 4)
        self.assertEqual(source.campaign.documents.count(), 4)
        self.assertEqual(source.status, FileSourceStatus.FINISHED)
    def test_processing_status_updated(self):
        setup_institutions()
        source = file_source_with_file()
        source.update_status = MagicMock()
        source.process()
        self.assertEqual(source.update_status.call_count, 2)
        args = [call.args[0] for call in source.update_status.call_args_list]
        self.assertEqual(args, [FileSourceStatus.PROCESSING, FileSourceStatus.FINISHED])


    def test_processing_wrong_schema(self):
        setup_institutions()
        source = file_source_with_wrong_data_file()
        source.process()

        source.refresh_from_db()
        self.assertEqual(source.campaign.documents.count(), 0)
        self.assertEqual(source.status, FileSourceStatus.FAILED)
