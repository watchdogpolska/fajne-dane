from rest_framework import serializers

from campaigns.models import Record
from campaigns.models.dto import RecordDTO
from campaigns.serializers.utils import get_source_serializer


class RecordSerializer(serializers.ModelSerializer):
    source = serializers.SerializerMethodField()

    class Meta:
        model = Record
        fields = ['id', 'value', 'probability', 'source', 'status', 'query']
        read_only_fields = ['id']
        extra_kwargs = {
            'query': {'write_only': True},
        }

    def get_source(self, obj):
        source = obj.source.to_child()
        serializer = get_source_serializer(source.type)
        return serializer(source).data

    def validate(self, attrs):
        query = attrs.get('query') or self.instance.query
        if 'value' in attrs:
            record_dto = RecordDTO(value=attrs['value'], probability=0)
            query.validate_record(record=record_dto)
        return super().validate(attrs)
