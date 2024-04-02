from rest_framework import serializers

from reports.models import TableComponent
from reports.serializers.data_view import DataViewSerializer


class TableComponentSerializer(serializers.ModelSerializer):
    data_view = DataViewSerializer(required=False)

    class Meta:
        model = TableComponent
        fields = ['id', 'name', 'type', 'title', 'columns', 'data_view', 'metadata']
        read_only_fields = ['id', 'data_view']

