from typing import List

from django.test import TestCase

from campaigns.models.dto import DocumentDTO
from campaigns.models.factory.documents_factory import DocumentsFactory
from tests.unit.campaigns.conftest import advanced_campaign_dataset
from tests.unit.campaigns.models.conftest import advanced_campaign_with_queries, basic_file_source, \
    advanced_campaign_documents_factory, advanced_campaign_data_frame_parser


def advanced_campaign_dtos() -> List[DocumentDTO]:
    parser = advanced_campaign_data_frame_parser()
    return parser.parse(advanced_campaign_dataset())


class CampaignFactoryTestCase(TestCase):

    def test_creating_factory(self):
        campaign = advanced_campaign_with_queries()
        source = basic_file_source()

        factory = DocumentsFactory(
            campaign=campaign,
            source=source
        )
        self.assertIsInstance(factory, DocumentsFactory)
        self.assertEqual(factory.campaign, campaign)
        self.assertEqual(factory.source, source)

    def test_creating_documents(self):
        factory = advanced_campaign_documents_factory()
        dtos = advanced_campaign_dtos()
        documents = factory.create(dtos)


