from fajne_dane.core.serializers import ReadOnlyModelSerializer
from reports.models.components import HTMLComponent


class HTMLComponentSerializer(ReadOnlyModelSerializer):
    class Meta:
        model = HTMLComponent
        fields = ['id', 'name', 'type', 'text']
