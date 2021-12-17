from django.test import TestCase

from campaigns.parsers.report import ParsingReport, DocumentError, ParsingError
from campaigns.serializers import ValidationErrorSerializer, DocumentErrorSerializer, DocumentFactoryReportSerializer
from tests.campaigns.conftest import advanced_campaign_data_frame_parser
from tests.conftest import wrong_advanced_campaign_dataset, advanced_campaign_dataset


def failed_parsing_report() -> ParsingReport:
    parser = advanced_campaign_data_frame_parser()
    df = wrong_advanced_campaign_dataset()
    report = parser.parse(df)
    return report


def valid_parsing_report() -> ParsingReport:
    parser = advanced_campaign_data_frame_parser()
    df = advanced_campaign_dataset()
    report = parser.parse(df)
    return report


def document_error() -> DocumentError:
    report = failed_parsing_report()
    return report.errors[0]


def parsing_error() -> ParsingError:
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
        serializer = DocumentErrorSerializer(error)

        self.assertEqual(serializer.data, {
            'index': 3,
            'data': {'institution_id': 28012},
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
        serializer = DocumentFactoryReportSerializer(report)

        self.assertEqual(serializer.data['is_valid'], False)
        self.assertEqual(serializer.data['documents_count'], 0)
        self.assertEqual(serializer.data, {
            'is_valid': False,
            'errors': [
                {
                    'index': 3,
                    'data': {'institution_id': 28012},
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
                        'institution_id': 1425011,
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
                    'data': {'institution_id': 1428022},
                    'errors': [
                        {
                            'code': 'missing-field',
                            'message': "Field: 'document_url' not found in the document data."
                        }
                    ]
                }
            ],
            'documents_count': 0
        })

    def test_serialize_valid(self):
        report = valid_parsing_report()
        serializer = DocumentFactoryReportSerializer(report)

        self.assertEqual(serializer.data['is_valid'], True)
        self.assertEqual(serializer.data['documents_count'], 4)
