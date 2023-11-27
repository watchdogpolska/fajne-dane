from rest_framework import generics
from rest_framework.permissions import AllowAny

from reports.models import DataSource
from reports.serializers.data_source import DataSourceSerializer


class DataSourceList(generics.ListAPIView):
    permission_classes = (AllowAny,)
    queryset = DataSource.objects.all()
    serializer_class = DataSourceSerializer
