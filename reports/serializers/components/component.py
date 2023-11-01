from fajne_dane.core.serializers import ReadOnlyModelSerializer
from reports.models.components import ReportComponent


class ReportComponentSerializer(ReadOnlyModelSerializer):
    class Meta:
        model = ReportComponent
        fields = ['id', 'name', 'type']
