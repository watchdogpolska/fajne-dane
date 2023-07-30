from django.test import TestCase

from campaigns.serializers import ValidationErrorSerializer, ParsingReportSerializer, DocumentParsingReportSerializer
from campaigns.validators.parsing_report import ParsingReport, DocumentParsingReport
from campaigns.validators.report import ValidationError
from tests.campaigns.conftest import advanced_campaign_data_frame_parser
from tests.conftest import wrong_advanced_campaign_dataset, advanced_campaign_dataset


def failed_parsing_report() -> ParsingReport:
    parser = advanced_campaign_data_frame_parser()
    df = wrong_advanced_campaign_dataset()
    report, _ = parser.parse(df)
    return report


def valid_parsing_report() -> ParsingReport:
    parser = advanced_campaign_data_frame_parser()
    df = advanced_campaign_dataset()
    report, _ = parser.parse(df)
    return report


def document_error() -> DocumentParsingReport:
    report = failed_parsing_report()
    return report.documents_errors[0]


def parsing_error() -> ValidationError:
    error = document_error()
    return error.errors[0]


class ErrorSerializerTestCase(TestCase):

    def test_serialize(self):
        error = parsing_error()
        serializer = ValidationErrorSerializer(error)

        self.assertEqual(serializer.data, {
            'code': 'missing-field',
            'message': "Field: 'document_url' not found in the document data."
        })


class DocumentErrorSerializerTestCase(TestCase):

    def test_serialize(self):
        error = document_error()
        serializer = DocumentParsingReportSerializer(error)

        self.assertEqual(serializer.data, {
            'index': 3,
            'data': {},
            'errors': [
                {
                    'code': 'missing-field',
                    'message': "Field: 'document_url' not found in the document data."
                },
                {
                    'code': 'invalid-value',
                    'message': "Record value: 'odpowiedź z poza zestawu.' not found in the list of accepted answers."
                }
            ]
        })


class DocumentFactoryReportSerializerTestCase(TestCase):

    def test_serialize(self):
        report = failed_parsing_report()
        serializer = ParsingReportSerializer(report)

        self.assertEqual(serializer.data['is_valid'], False)
        self.assertEqual(serializer.data['valid_documents_count'], 1)
        self.assertEqual(serializer.data['invalid_documents_count'], 3)
        self.assertEqual(serializer.data, {
            'is_valid': False,
            'file_errors': [],
            'documents_errors': [
                {
                    'index': 3,
                    'data': {},
                    'errors': [
                        {
                            'code': 'missing-field',
                            'message': "Field: 'document_url' not found in the document data."
                        },
                        {
                            'code': 'invalid-value',
                            'message': "Record value: 'odpowiedź z poza zestawu.' not found in the list of accepted answers."
                        }
                    ]
                },
                {
                    'index': 2,
                    'data': {
                        'document_url': 'https://funcrowd-documents.sprawdzamyjakjest.pl/static/pdf/monitoring42/34181.pdf'
                    },
                    'errors': [
                        {
                            'code': 'invalid-value',
                            'message': "Record value: 'nie jestem do końca pewien' not found in the list of accepted answers."
                        }
                    ]
                },
                {
                    'index': 1,
                    'data': {},
                    'errors': [
                        {
                            'code': 'missing-field',
                            'message': "Field: 'document_url' not found in the document data."
                        }
                    ]
                }
            ],
            'valid_documents_count': 1,
            'invalid_documents_count': 3
        })

    def test_serialize_valid(self):
        report = valid_parsing_report()
        serializer = ParsingReportSerializer(report)

        self.assertEqual(serializer.data['is_valid'], True)
        self.assertEqual(serializer.data['valid_documents_count'], 4)
        self.assertEqual(serializer.data['invalid_documents_count'], 0)
