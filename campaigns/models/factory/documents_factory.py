from dataclasses import dataclass
from typing import List

from lib.base.factory import BaseFactory
from .. import Campaign, Document, Query, Record, Source
from ..dto import DocumentDTO, RecordDTO




@dataclass
class DocumentsFactory(BaseFactory):
    campaign: Campaign
    source: Source

    def _create_campaign_document(self, document_dto: DocumentDTO) -> Document:
        return Document(
            campaign=self.campaign,
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

    def bulk_create(self, documents_dto: List[DocumentDTO]) -> List[Document]:
        raise NotImplemented

    def create(self, document_dto: DocumentDTO) -> Document:
        queries = {q.name: q for q in self.campaign.queries.all()}

        document = self._create_campaign_document(document_dto).save()
        records = []
        for query_name, query in queries:
            record_dto = document_dto.records.get(query_name)
            if not record_dto:
                continue
            records.append(self._create_document_query_record(document, query, record_dto))
        Record.objects.bulk_create(records)
        return document
