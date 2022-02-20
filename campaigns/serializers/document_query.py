from campaigns.models import DocumentQuery
from campaigns.serializers import QueryDataSerializer, RecordSerializer, QuerySerializer
from fajne_dane.core.serializers import ReadOnlyModelSerializer


class DocumentQuerySerializer(ReadOnlyModelSerializer):
    query = QueryDataSerializer(read_only=True)

    class Meta:
        model = DocumentQuery
        fields = ('id', 'query', 'status')
        read_only_fields = ['id', 'query', 'status']


class DocumentQueryFullSerializer(ReadOnlyModelSerializer):
    query = QuerySerializer(read_only=True)
    records = RecordSerializer(read_only=True, many=True)
    accepted_record = RecordSerializer(read_only=True)

    class Meta:
        model = DocumentQuery
        fields = ('id', 'query', 'status', 'records', 'accepted_record')
        read_only_fields = ['id', 'query', 'status', 'records', 'accepted_record']


class DocumentQueryStatusSerializer(ReadOnlyModelSerializer):
    class Meta:
        model = DocumentQuery
        fields = ('id', 'status')
        read_only_fields = ['id', 'status']
