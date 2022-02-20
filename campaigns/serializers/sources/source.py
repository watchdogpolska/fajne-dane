from campaigns.models import Source
from fajne_dane.core.serializers import ReadOnlyModelSerializer


class SourceSerializer(ReadOnlyModelSerializer):
    class Meta:
        model = Source
        fields = ['id', 'name', 'type']
