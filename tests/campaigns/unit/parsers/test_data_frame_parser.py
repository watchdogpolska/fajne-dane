from django.test import TestCase

from campaigns.models.dto import DocumentDTO
from campaigns.parsers.data_frame_parser import DataFrameParser
from tests.conftest import (
    advanced_campaign_dataset, wrong_advanced_campaign_dataset, basic_campaign_dataset
)
from tests.campaigns.conftest import (
    advanced_campaign_with_queries,
    advanced_campaign_data_frame_parser,
    basic_campaign_data_frame_parser
)


class CampaignFactoryTestCase(TestCase):

    def test_creating_parser(self):
        campaign = advanced_campaign_with_queries()
        parser = DataFrameParser(
            campaign=campaign
        )
        self.assertIsInstance(parser, DataFrameParser)
        self.assertEqual(parser.campaign, campaign)

    def test_parse_basic_data_frame(self):
        parser = basic_campaign_data_frame_parser()
        df = basic_campaign_dataset()
        report = parser.parse(df)

        self.assertTrue(report.is_valid)
        document_dtos = report.documents

        self.assertEqual(len(document_dtos), 4)
        for document_dto, expected_records_values_count in zip(document_dtos, [[1], [2], [1], [1]]):
            self.assertIsInstance(document_dto, DocumentDTO)

            records_values_counts = [len(v) for v in document_dto.records.values()]
            self.assertEqual(records_values_counts, expected_records_values_count)

    def test_parse_advanced_data_frame(self):
        parser = advanced_campaign_data_frame_parser()
        df = advanced_campaign_dataset()
        report = parser.parse(df)

        self.assertTrue(report.is_valid)
        document_dtos = report.documents

        self.assertEqual(len(document_dtos), 4)
        for document_dto, expected_records_values_count in \
                zip(document_dtos, [[1, 0, 0], [1, 1, 2], [1, 1, 1], [1, 1, 1]]):
            self.assertIsInstance(document_dto, DocumentDTO)

            records_values_counts = [len(v) for v in document_dto.records.values()]
            self.assertEqual(records_values_counts, expected_records_values_count)

    def test_parse_wrong_data_frame(self):
        parser = advanced_campaign_data_frame_parser()
        df = wrong_advanced_campaign_dataset()
        report = parser.parse(df)

        self.assertFalse(report.is_valid)
        self.assertEqual(len(report.errors), 3)

        expected_error_codes = {
            1: ['missing-field'],
            2: ['invalid-value'],
            3: ['missing-field', 'invalid-value']
        }

        for error in report.errors:
            self.assertEqual(
                [e.code for e in error.errors],
                expected_error_codes[error.index]
            )
