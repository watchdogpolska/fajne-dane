from rest_framework import serializers
from fajne_dane.core.serializers import (
    ReadCreateModelSerializer,
)
from reports.models import (
    DataView,
    DataSource,
)
from reports.serializers.data_source import DataSourceSerializer


class DataViewSerializer(ReadCreateModelSerializer):
    file_url = serializers.SerializerMethodField()
    data_source = DataSourceSerializer()
    class Meta:
        model = DataView
        fields = ['id', 'name', 'type', 'keys', 'keys_labels', 'values', 'values_labels', 'aggregation', 'data_source', 'file_url']
        read_only_fields = ['id', 'data_source', 'type', 'file_url', 'keys_labels', 'values_labels']

    def get_file_url(self, obj):
        return obj.file.url


class DataViewCreateSerializer(ReadCreateModelSerializer):
    data_source_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = DataView
        fields = ['name', 'type', 'keys', 'values', 'aggregation', 'data_source_id']
