from typing import List

from django.test import TestCase

from campaigns.models import Document, Record
from campaigns.models.consts import RecordStatus, CampaignStatus, DocumentQueryStatus, DocumentStatus
from campaigns.models.dto import DocumentDTO
from campaigns.models.factory.documents_factory import DocumentsFactory
from tests.campaigns.conftest import (
    advanced_campaign_dtos,
    advanced_campaign_with_queries,
    basic_file_source,
    advanced_campaign_documents_factory, setup_institutions
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


class CampaignFactoryCreatingTestCase(TestCase):
    def setUp(self):
        setup_institutions()
        self.factory = advanced_campaign_documents_factory()
        self.campaign = self.factory.campaign

    def test_creating_documents(self):
        """Test creating a single Document object"""
        document_dtos = advanced_campaign_dtos()
        documents = [
            self.factory.create(document_dto)
            for document_dto in document_dtos
        ]
        self._compare_documents_with_dtos(documents, document_dtos)
        self._test_statuses(documents)

    def test_bulk_creating_documents(self):
        """Test creating multiple Document objects in a bulk"""
        document_dtos = advanced_campaign_dtos()
        documents = self.factory.bulk_create(document_dtos)
        self._compare_documents_with_dtos(documents, document_dtos)

    def _compare_documents_with_dtos(self, documents: List[Document], document_dtos: List[DocumentDTO]):
        """Utils function used to compare created Document objects with DocumentDTO"""
        for document, document_dto in zip(documents, document_dtos):
            self.assertIsInstance(document, Document)
            self.assertEqual(document.data, document_dto.data)

            for query_name, records_dtos in document_dto.records.items():
                document_queries = document.document_queries.filter(query__name=query_name).first()
                records = document_queries.records.all()
                for record, record_dto in zip(records, records_dtos):
                    self.assertEqual(record.value, record_dto.value)
                    self.assertEqual(record.probability, record_dto.probability)

    def _test_statuses(self, documents: List[Document]):
        for document in documents:
            if document.document_queries.count() > 0:
                if document.document_queries.exclude(status=DocumentQueryStatus.CLOSED).count() == 0:
                    self.assertEqual(document.status, DocumentStatus.CLOSED)
                elif document.document_queries.filter(status=DocumentQueryStatus.CLOSED).count() > 0:
                    self.assertEqual(document.status, DocumentStatus.VALIDATING)
                else:
                    self.assertEqual(document.status, DocumentStatus.INITIALIZED)
            else:
                self.assertEqual(document.status, DocumentStatus.CREATED)

            for dq in document.document_queries.all():
                if dq.records.count() > 0:
                    if dq.accepted_record:
                        self.assertEqual(dq.status, DocumentQueryStatus.CLOSED)
                    else:
                        self.assertEqual(dq.status, DocumentQueryStatus.INITIALIZED)
                else:
                    self.assertEqual(dq.status, DocumentQueryStatus.CREATED)

                for record in dq.records.all():
                    if record.probability > 0.5:
                        self.assertEqual(record.status, RecordStatus.ACCEPTED)
                    else:
                        self.assertEqual(record.status, RecordStatus.NONE)

        self.assertEqual(self.campaign.status, CampaignStatus.VALIDATING)
