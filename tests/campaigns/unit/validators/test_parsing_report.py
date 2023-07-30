from django.test import TestCase

from campaigns.validators.parsing_report import DocumentParsingReport, ParsingReport
from campaigns.validators.report import ValidationError as DocumentParsingError


def test_invalid_document_report() -> DocumentParsingReport:
    return DocumentParsingReport(
        index=12,
        data={},
        errors=[
            DocumentParsingError("parsing error", "error message"),
            DocumentParsingError("parsing error", "other error message")
        ]
    )


class DocumentParsingReportTestCase(TestCase):
    def test_create_parsing_error_valid(self):
        report = DocumentParsingReport(index=12, data={}, errors=[])
        self.assertIsInstance(report, DocumentParsingReport)
        self.assertEqual(report.index, 12)
        self.assertEqual(report.data, {})
        self.assertTrue(report.is_valid)

    def test_prepare_validation_error_invalid(self):
        report = test_invalid_document_report()
        self.assertFalse(report.is_valid)


class ParsingReportTestCase(TestCase):
    def test_create_parsing_error_valid(self):
        report = ParsingReport(file_errors=[], valid_documents_count=0, documents_errors=[])
        self.assertIsInstance(report, ParsingReport)
        self.assertTrue(report.is_valid)
        self.assertEqual(report.invalid_documents_count, 0)

    def test_prepare_validation_error_invalid(self):
        report = ParsingReport(
            file_errors=[],
            valid_documents_count=0,
            documents_errors=[
                test_invalid_document_report()
            ]
        )
        self.assertFalse(report.is_valid)
        self.assertEqual(report.invalid_documents_count, 1)
