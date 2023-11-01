from fajne_dane.core.serializers import ReadOnlyModelSerializer
from reports.models import TableComponent


class TableComponentSerializer(ReadOnlyModelSerializer):
    class Meta:
        model = TableComponent
        fields = ['id', 'name', 'type', 'data_url', 'title', 'columns']
        read_only_field = ['id', 'name', 'type', 'data_url', 'title', 'columns']

