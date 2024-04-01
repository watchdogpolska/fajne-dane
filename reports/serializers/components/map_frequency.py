from fajne_dane.core.serializers import ReadOnlyModelSerializer
from reports.models import MapFrequencyComponent
from reports.serializers.data_view import DataViewSerializer


class MapFrequencyComponentSerializer(ReadOnlyModelSerializer):
    data_view = DataViewSerializer()

    class Meta:
        model = MapFrequencyComponent
        fields = ['id', 'name', 'type', 'title', 'index', 'value', 'data_view']
        read_only_fields = ['id', 'name', 'type', 'title', 'index', 'value', 'data_view']
