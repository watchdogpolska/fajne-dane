from dataclasses import dataclass
from typing import List

from fajne_dane.core.base.factory import BaseFactory
from .. import Campaign, Document, Query, Record, FileSource
from ..dto import DocumentDTO, RecordDTO


@dataclass
class DocumentsFactory(BaseFactory):
    campaign: Campaign
    source: FileSource

    def _create_campaign_document(self, document_dto: DocumentDTO) -> Document:
        return Document(
            campaign=self.source.campaign,
            source=self.source,
            data=document_dto.data
        )

    def _create_document_query_record(self, document: Document, query: Query, record_dto: RecordDTO) -> Record:
        return Record(
            document=document,
            query=query,
            source=self.source,
            value=record_dto.value,
            probability=record_dto.probability
    )

    def bulk_create(self, document_dtos: List[DocumentDTO]) -> List[Document]:
        """
        Creates a list of Document and their Records in bulk, based on provided list of DocumentDTOs.

        :param document_dtos: a list of documents' DTOs
        :returns: a list of created and saved Document objects
        """
        queries = {q.name: q for q in self.campaign.queries_objects}

        # create documents
        documents = []
        for document_dto in document_dtos:
            documents.append(self._create_campaign_document(document_dto))
        documents = Document.objects.bulk_create(documents)

        # create records
        records = []
        for document, dto in zip(documents, document_dtos):
            for query_name, query in queries.items():
                records_dtos = dto.records.get(query_name)
                for record_dto in records_dtos:
                    records.append(self._create_document_query_record(document, query, record_dto))
        Record.objects.bulk_create(records)
        return documents

    def create(self, document_dto: DocumentDTO) -> Document:
        """
        Creates Document and its Records based on provided DocumentDTO

        :param document_dto: dto of the document
        :returns: created and saved Document object
        """
        queries = {q.name: q for q in self.campaign.queries_objects}

        # create the document
        document = self._create_campaign_document(document_dto)
        document.save()

        # create records
        records = []
        for query_name, query in queries.items():
            records_dtos = document_dto.records.get(query_name)
            for record_dto in records_dtos:
                records.append(self._create_document_query_record(document, query, record_dto))
        Record.objects.bulk_create(records)
        return document
