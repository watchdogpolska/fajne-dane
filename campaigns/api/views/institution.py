from rest_framework import generics, status
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.response import Response

from campaigns.api.exceptions import InstitutionHasDocuments
from campaigns.api.views.config import StandardResultsSetPagination
from campaigns.models import Institution, Document
from campaigns.serializers import InstitutionSerializer, InstitutionCreateSerializer, InstitutionDetailsSerializer
from rest_framework import filters


class CustomInstitutionFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        _query = request.query_params.get("query")
        _order = request.query_params.get("order", "name")

        queryset = queryset.order_by(_order)
        if _query:
            queryset = queryset.filter(name__icontains=_query)
        return queryset


class InstitutionList(generics.ListAPIView):
    serializer_class = InstitutionSerializer
    permission_classes = (AllowAny,)
    filter_backends = [CustomInstitutionFilterBackend]
    search_fields = ['name', 'key']
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        group_id = self.kwargs.get("group_id")
        return Institution.objects.filter(group_id=group_id)



class InstitutionDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = InstitutionDetailsSerializer
    permission_classes = (IsAdminUser,)
    queryset = Institution.objects.all()

    def delete(self, request, *args, **kwargs):
        documents = Document.objects.filter(institution__id=kwargs['pk'])
        if documents.count():
            raise InstitutionHasDocuments()
        return super().delete(request)


class InstitutionCreate(generics.CreateAPIView):
    serializer_class = InstitutionCreateSerializer
    permission_classes = (IsAdminUser,)
    queryset = Institution.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            instance = serializer.save(group_id=self.kwargs['group_id'])
            output_serializer = self.get_serializer(instance)
            headers = self.get_success_headers(output_serializer.data)
            return Response(output_serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
