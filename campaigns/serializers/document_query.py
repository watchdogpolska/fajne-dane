from campaigns.models import DocumentQuery
from campaigns.serializers import QueryDataSerializer, RecordSerializer, QuerySerializer, QueryOrderSerializer
from fajne_dane.core.serializers import ReadOnlyModelSerializer, serializers


class DocumentQuerySerializer(ReadOnlyModelSerializer):
    query = QueryDataSerializer(read_only=True)

    class Meta:
        model = DocumentQuery
        fields = ('id', 'query', 'status')
        read_only_fields = ['id', 'query', 'status']


class DocumentQueryFullSerializer(ReadOnlyModelSerializer):
    query = QuerySerializer(read_only=True)
    records = RecordSerializer(read_only=True, many=True)
    accepted_records = RecordSerializer(read_only=True, many=True)

    class Meta:
        model = DocumentQuery
        fields = ('id', 'query', 'status', 'records', 'accepted_records')
        read_only_fields = ['id', 'query', 'status', 'records', 'accepted_records']


class DocumentQueryStatusSerializer(ReadOnlyModelSerializer):
    query = QueryOrderSerializer(read_only=True)

    class Meta:
        model = DocumentQuery
        fields = ('id', 'status', 'query')
        read_only_fields = ['id', 'status', 'query']
