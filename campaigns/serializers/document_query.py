from campaigns.models import DocumentQuery
from campaigns.serializers import QueryDataSerializer
from fajne_dane.core.serializers import ReadOnlyModelSerializer


class DocumentQuerySerializer(ReadOnlyModelSerializer):
    query = QueryDataSerializer(read_only=True)

    class Meta:
        model = DocumentQuery
        fields = ('id', 'query', 'status')
        read_only_fields = ['id', 'query', 'status']
