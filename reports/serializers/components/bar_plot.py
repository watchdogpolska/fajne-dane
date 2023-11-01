from fajne_dane.core.serializers import ReadOnlyModelSerializer
from reports.models import BarPlotComponent


class BarPlotComponentSerializer(ReadOnlyModelSerializer):
    class Meta:
        model = BarPlotComponent
        fields = ['id', 'name', 'type', 'data_url', 'title', 'index', 'value']
        read_only_field = ['id', 'name', 'type', 'data_url', 'title', 'index', 'value']

