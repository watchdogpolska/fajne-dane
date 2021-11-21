from django.test import TestCase

from campaigns.models import Document
from campaigns.models.factory.documents_factory import DocumentsFactory
from tests.campaigns.conftest import (
    advanced_campaign_dtos,
    advanced_campaign_with_queries,
    basic_file_source,
    advanced_campaign_documents_factory
)


class CampaignFactoryTestCase(TestCase):

    def test_creating_factory(self):
        """Test creating a DocumentsFactory object"""
        campaign = advanced_campaign_with_queries()
        source = basic_file_source(campaign)

        factory = DocumentsFactory(
            campaign=campaign,
            source=source
        )
        self.assertIsInstance(factory, DocumentsFactory)
        self.assertEqual(factory.campaign, campaign)
        self.assertEqual(factory.source, source)

    def _compare_documents_with_dtos(self, documents, document_dtos):
        """Utils function used to compare created Document objects with DocumentDTO"""
        for document, document_dto in zip(documents, document_dtos):
            self.assertIsInstance(document, Document)
            self.assertEqual(document.data, document_dto.data)

            for query_name, records_dtos in document_dto.records.items():
                records = document.records.filter(query__name=query_name)
                for record, record_dto in zip(records, records_dtos):
                    self.assertEqual(record.value, record_dto.value)
                    self.assertEqual(record.probability, record_dto.probability)


    def test_creating_documents(self):
        """Test creating a single Document object"""
        factory = advanced_campaign_documents_factory()
        document_dtos = advanced_campaign_dtos()
        documents = [
            factory.create(document_dto)
            for document_dto in document_dtos
        ]
        self._compare_documents_with_dtos(documents, document_dtos)

    def test_bulk_creating_documents(self):
        """Test creating multiple Document objects in a bulk"""
        factory = advanced_campaign_documents_factory()
        document_dtos = advanced_campaign_dtos()
        documents = factory.bulk_create(document_dtos)
        self._compare_documents_with_dtos(documents, document_dtos)
