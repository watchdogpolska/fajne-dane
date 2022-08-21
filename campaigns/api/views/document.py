from collections import OrderedDict

from django.db.models import Count
from rest_framework import filters
from rest_framework import generics, status, views
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response

from campaigns.models import Document, UserSource, Campaign
from campaigns.models.consts import DocumentStatus
from campaigns.models.dto import DocumentDTO
from campaigns.models.factory.documents_factory import DocumentsFactory
from campaigns.serializers import (
    DocumentSerializer, DocumentCreateSerializer, DocumentFullSerializer, IdListSerializer, DocumentIdSerializer
)


def get_frequency_list(queryset, column):
    frequency = queryset.values(column) \
        .order_by(column) \
        .annotate(count=Count(column))
    return {
        r[column]: r['count']
        for r in frequency
    }


class StandardResultsSetPagination(LimitOffsetPagination):
    page_size = 10
    page_size_query_param = 'limit'
    max_page_size = 100


class CustomFilterBackend(filters.BaseFilterBackend):
    """
    Filter that only allows users to see their own objects.
    """
    def filter_queryset(self, request, queryset, view):
        _query = request.query_params.get("query")
        _order = request.query_params.get("order", "created")
        _status = request.query_params.get("status")

        queryset = queryset.order_by(_order)
        if _query:
            queryset = queryset.filter(institution__name__icontains=_query)
        if _status:
            queryset = queryset.filter(status=_status)
        return queryset


class DocumentList(generics.ListAPIView):
    serializer_class = DocumentSerializer
    permission_classes = (AllowAny,)
    filter_backends = [CustomFilterBackend]
    search_fields = ['query', 'order', 'status']
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        campaign_id = self.kwargs.get("campaign_id")
        return Document.objects.filter(campaign_id=campaign_id)


class DocumentsStatusList(generics.ListAPIView):
    permission_classes = (AllowAny,)
    filter_backends = [CustomFilterBackend]
    search_fields = ['query']

    def get_queryset(self):
        campaign_id = self.kwargs.get("campaign_id")
        return Document.objects.filter(campaign_id=campaign_id)

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        frequency = get_frequency_list(queryset, "status")
        return Response(frequency, status=status.HTTP_201_CREATED)


class DocumentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentFullSerializer
    permission_classes = (IsAdminUser,)


class DocumentCreate(generics.CreateAPIView):
    serializer_class = DocumentCreateSerializer
    permission_classes = (IsAdminUser,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        campaign = Campaign.objects.get(id=self.kwargs['campaign_id'])
        source, created = UserSource.objects.get_or_create(user=request.user)
        if created:
            source.name = f"{request.user.first_name} {request.user.last_name}"
            source.save()

        dto = DocumentDTO(data=serializer.validated_data['data'])

        factory = DocumentsFactory(campaign=campaign, source=source)
        document = factory.create(dto)

        serializer = self.get_serializer(document)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class DocumentBulkDelete(views.APIView):
    permission_classes = (IsAdminUser,)
    serializer_class = IdListSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            documents = Document.objects.filter(id__in=serializer.validated_data['ids'])
            documents.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
class GetUnsolvedDocument(generics.RetrieveAPIView):
    permission_classes = (IsAdminUser,)
    serializer_class = DocumentIdSerializer

    def get_object(self):
        campaign_id = self.kwargs.get("pk")
        return Document.objects \
            .filter(campaign_id=campaign_id) \
            .exclude(status__in=[DocumentStatus.CLOSED]).first()
