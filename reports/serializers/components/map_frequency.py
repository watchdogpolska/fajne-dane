from fajne_dane.core.serializers import ReadOnlyModelSerializer
from reports.models import MapFrequencyComponent


class MapFrequencyComponentSerializer(ReadOnlyModelSerializer):
    class Meta:
        model = MapFrequencyComponent
        fields = ['id', 'name', 'type', 'data_url', 'title', 'index', 'value']
        read_only_field = ['id', 'name', 'type', 'data_url', 'title', 'index', 'value']


