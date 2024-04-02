from rest_framework import generics

from campaigns.models import DocumentQuery
from campaigns.serializers import DocumentQueryFullSerializer, DocumentQueryStatusSerializer


class DocumentQueryDetail(generics.RetrieveAPIView):
    queryset = DocumentQuery.objects.all()
    serializer_class = DocumentQueryFullSerializer


class DocumentQueryStatusList(generics.ListAPIView):
    serializer_class = DocumentQueryStatusSerializer

    def get_queryset(self):
        document_id = self.kwargs.get("pk")
        return DocumentQuery.objects.filter(document_id=document_id)
