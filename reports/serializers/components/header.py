from fajne_dane.core.serializers import ReadOnlyModelSerializer
from reports.models.components import HeaderComponent


class HeaderComponentSerializer(ReadOnlyModelSerializer):
    class Meta:
        model = HeaderComponent
        fields = ['id', 'name', 'type', 'title', 'subtitle']
