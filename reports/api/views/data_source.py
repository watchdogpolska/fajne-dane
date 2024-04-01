from rest_framework import generics

from fajne_dane.core import IsAdminOrReadOnly
from reports.models import DataSource
from reports.serializers.data_source import (
    DataSourceSerializer,
    DataSourceFullSerializer,
)


class DataSourceList(generics.ListAPIView):
    permission_classes = (IsAdminOrReadOnly,)
    queryset = DataSource.objects.all()
    serializer_class = DataSourceSerializer


class DataSourceDetails(generics.RetrieveAPIView):
    permission_classes = (IsAdminOrReadOnly,)
    queryset = DataSource.objects.all()
    serializer_class = DataSourceFullSerializer

