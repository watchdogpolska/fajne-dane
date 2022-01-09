from typing import Dict

from rest_framework import serializers

from campaigns.models import Record, DocumentQuery
from campaigns.models.dto import RecordDTO
from campaigns.serializers.sources.utils import get_source_serializer


def _validate_attrs(document_query: DocumentQuery, attrs: Dict):
    if 'value' in attrs:
        record_dto = RecordDTO(value=attrs['value'], probability=0)
        document_query.query.validate_record(record=record_dto)


class RecordSerializer(serializers.ModelSerializer):
    source = serializers.SerializerMethodField()

    class Meta:
        model = Record
        fields = ['id', 'value', 'probability', 'source', 'status', 'parent']
        read_only_fields = ['id']
        extra_kwargs = {
            'parent': {'write_only': True},
        }

    def get_source(self, obj):
        source = obj.source.to_child()
        serializer = get_source_serializer(source.type)
        return serializer(source).data

    def validate(self, attrs):
        if self.instance:
            document_query = self.instance.parent
        else:
            document_query = attrs.get('parent')
        _validate_attrs(document_query, attrs)
        return super().validate(attrs)
