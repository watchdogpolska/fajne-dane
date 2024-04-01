from fajne_dane.core.serializers import ReadCreateModelSerializer
from reports.models import BarPlotComponent
from reports.serializers.data_view import DataViewSerializer


class BarPlotComponentSerializer(ReadCreateModelSerializer):
    data_view = DataViewSerializer(required=False)

    class Meta:
        model = BarPlotComponent
        fields = ['id', 'name', 'type', 'title', 'index', 'value', 'data_view']
        read_only_fields = ['id', 'data_view']

