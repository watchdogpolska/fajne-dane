from dataclasses import dataclass
from django.db import transaction
from typing import List

from fajne_dane.core.base.factory import BaseFactory
from .. import Campaign, Document, Query, Record, DocumentQuery, Institution, Source
from ..dto import DocumentDTO, RecordDTO, InstitutionDTO
from ...exceptions import DocumentInstitutionMissmatch


def get_institution(dto: InstitutionDTO):
    if dto.id:
        return Institution.objects.get(id=dto.id)
    return Institution.objects.get(key=dto.key)


@dataclass
class DocumentsFactory(BaseFactory):
    campaign: Campaign
    source: Source


    def _create_campaign_document(self, document_dto: DocumentDTO) -> Document:
        institution = get_institution(document_dto.institution)
        if institution.group.id not in self.campaign.institution_groups_path:
            raise DocumentInstitutionMissmatch()
        return Document(
            campaign=self.campaign,
            source=self.source,
            data=document_dto.data,
            institution=institution
        )

    def _create_document_query(self, document: Document, query: Query) -> DocumentQuery:
        return DocumentQuery(
            document=document,
            query=query
        )

    def _create_record(self, document_query: DocumentQuery, record_dto: RecordDTO) -> Record:
        return Record(
            parent=document_query,
            source=self.source,
            value=record_dto.value,
            probability=record_dto.probability
        )

    @transaction.atomic
    def bulk_create(self, document_dtos: List[DocumentDTO]) -> List[Document]:
        """
        Creates a list of Document and their Records in bulk, based on provided list of DocumentDTOs.

        :param document_dtos: a list of documents' DTOs
        :returns: a list of created and saved Document objects
        """
        queries = {q.name: q for q in self.campaign.queries_objects}

        documents = [
            self._create_campaign_document(document_dto)
            for document_dto in document_dtos
        ]
        documents = Document.objects.bulk_create(documents)

        # create document queries
        document_queries = []
        for document, dto in zip(documents, document_dtos):
            document_queries.extend(
                self._create_document_query(document, query)
                for query in queries.values()
            )
        document_queries = {
            (dq.document.id, dq.query.id): dq
            for dq in DocumentQuery.objects.bulk_create(document_queries)
        }

        # create records
        records = []
        for document, dto in zip(documents, document_dtos):
            for query_name, query in queries.items():
                records_dtos = dto.records.get(query_name, [])
                document_query = document_queries[(document.id, query.id)]
                records.extend(
                    self._create_record(document_query, record_dto)
                    for record_dto in records_dtos
                )
        Record.objects.bulk_create(records)

        # update status:
        for dq in document_queries.values():
            selected_records = dq.records.filter(probability__gt=0.5)
            if selected_records and ((dq.query.output_field.type == 'list') or (selected_records.count() == 1)):
                dq.accept_records(selected_records)
            dq.update_status()

        # update data source
        self.campaign.update_data_source()
        return documents

    @transaction.atomic
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

        document_queries = [
            self._create_document_query(document, query)
            for query in queries.values()
        ]
        document_queries = {
            (dq.document.id, dq.query.id): dq
            for dq in DocumentQuery.objects.bulk_create(document_queries)
        }

        # create records
        records = []
        for query_name, query in queries.items():
            records_dtos = document_dto.records.get(query_name, [])
            document_query = document_queries[(document.id, query.id)]
            records.extend(
                self._create_record(document_query, record_dto)
                for record_dto in records_dtos
            )
        Record.objects.bulk_create(records)

        # update status:
        for dq in document_queries.values():
            selected_records = dq.records.filter(probability__gt=0.5)
            if selected_records.count() and \
                        ((dq.query.output_field.type == 'list') or (selected_records.count() == 1)):
                dq.accept_records(selected_records)
            dq.update_status()
        return document
