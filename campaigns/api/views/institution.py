from rest_framework import generics, status, views
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.response import Response

from campaigns.api.exceptions import InstitutionHasDocuments
from campaigns.api.views.config import StandardResultsSetPagination
from campaigns.models import Institution, Document
from campaigns.serializers import InstitutionSerializer, InstitutionCreateSerializer, InstitutionDetailsSerializer, \
    IdListSerializer
from rest_framework import filters

from campaigns.serializers.institutions import InstitutionDataSerializer


class CustomInstitutionFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        _query = request.query_params.get("query")
        _key = request.query_params.get("key")
        _order = request.query_params.get("order", "name")
        queryset = queryset.order_by(_order)
        if _query:
            queryset = queryset.filter(name__icontains=_query)
        if _key:
            queryset = queryset.filter(key__icontains=_key)
        return queryset


class InstitutionList(generics.ListAPIView):
    serializer_class = InstitutionDataSerializer
    permission_classes = (AllowAny,)
    filter_backends = [CustomInstitutionFilterBackend]
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


class InstitutionBulkDelete(views.APIView):
    permission_classes = (IsAdminUser,)
    serializer_class = IdListSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            institutions = Institution.objects.filter(id__in=serializer.validated_data['ids'])
            if Document.objects.filter(institution__in=institutions).count():
                raise InstitutionHasDocuments()
            institutions.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


