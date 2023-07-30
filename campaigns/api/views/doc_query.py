from rest_framework import generics
from rest_framework.permissions import IsAdminUser

from campaigns.models import DocumentQuery
from campaigns.serializers import DocumentQueryFullSerializer, DocumentQueryStatusSerializer


class DocumentQueryDetail(generics.RetrieveAPIView):
    queryset = DocumentQuery.objects.all()
    serializer_class = DocumentQueryFullSerializer
    permission_classes = (IsAdminUser,)


class DocumentQueryStatusList(generics.ListAPIView):
    serializer_class = DocumentQueryStatusSerializer
    permission_classes = (IsAdminUser,)

    def get_queryset(self):
        document_id = self.kwargs.get("pk")
        return DocumentQuery.objects.filter(document_id=document_id)
