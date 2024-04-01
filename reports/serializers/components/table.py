from fajne_dane.core.serializers import ReadOnlyModelSerializer
from reports.models import TableComponent
from reports.serializers.data_view import DataViewSerializer


class TableComponentSerializer(ReadOnlyModelSerializer):
    data_view = DataViewSerializer()

    class Meta:
        model = TableComponent
        fields = ['id', 'name', 'type', 'title', 'columns', 'data_view']
        read_only_fields = ['id', 'name', 'type', 'title', 'columns', 'data_view']

