from rest_framework import generics

from campaigns.api.exceptions import InstitutionGroupHasDocuments
from campaigns.models import InstitutionGroup, Document
from campaigns.serializers import (
    InstitutionGroupSerializer,
    InstitutionGroupCreateSerializer,
    InstitutionGroupDetailsSerializer
)
from fajne_dane.core import IsAdminOrReadOnly


class InstitutionGroupList(generics.ListAPIView):
    serializer_class = InstitutionGroupSerializer
    permission_classes = (IsAdminOrReadOnly,)
    queryset = InstitutionGroup.objects.all()


class InstitutionGroupCreate(generics.CreateAPIView):
    serializer_class = InstitutionGroupCreateSerializer
    permission_classes = (IsAdminOrReadOnly,)
    queryset = InstitutionGroup.objects.all()


class InstitutionGroupDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = InstitutionGroupDetailsSerializer
    permission_classes = (IsAdminOrReadOnly,)
    queryset = InstitutionGroup.objects.all()

    def delete(self, request, *args, **kwargs):
        documents = Document.objects.filter(institution__group__id=kwargs['pk'])
        if documents.count():
            raise InstitutionGroupHasDocuments()
        return super().delete(request)
