from django.test import TestCase

from campaigns.models.dto import InstitutionDTO
from campaigns.parsers import institutions_file_parser
from tests.conftest import (
    basic_institutions_file
)


class CampaignDatasetParserTestCase(TestCase):

    def test_creating_parse(self):
        institutions_file = basic_institutions_file()
        dtos = institutions_file_parser.parse(institutions_file)

        for dto in dtos:
            self.assertIsInstance(dto, InstitutionDTO)

        self.assertEqual(len(dtos), len(institutions_file))
