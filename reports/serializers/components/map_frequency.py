from rest_framework import serializers

from reports.models import MapFrequencyComponent
from reports.serializers.data_view import DataViewSerializer


class MapFrequencyComponentSerializer(serializers.ModelSerializer):
    data_view = DataViewSerializer(required=False)

    class Meta:
        model = MapFrequencyComponent
        fields = ['id', 'name', 'type', 'title', 'index', 'value', 'data_view', 'metadata']
        read_only_fields = ['id', 'data_view']
