from rest_framework import serializers
from reports.models import BarPlotComponent
from reports.serializers.data_view import DataViewSerializer


class BarPlotComponentSerializer(serializers.ModelSerializer):
    data_view = DataViewSerializer(required=False)

    class Meta:
        model = BarPlotComponent
        fields = ['id', 'name', 'type', 'title', 'index', 'value', 'data_view', 'metadata']
        read_only_fields = ['id', 'data_view']

