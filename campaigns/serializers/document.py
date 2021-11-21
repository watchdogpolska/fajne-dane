from typing import Dict

from rest_framework import serializers
from campaigns.models import Document, Campaign
from campaigns.models.dto import DocumentDTO
from campaigns.serializers.utils import get_source_serializer
from fajne_dane.core.exceptions import NotSupported

def _validate_attrs(campaign: Campaign, attrs: Dict):
    if 'data' in attrs:
        document_dto = DocumentDTO(data=attrs['data'])
        campaign.validate_document(document_dto)


class DocumentSerializer(serializers.ModelSerializer):
    source = serializers.SerializerMethodField()

    class Meta:
        model = Document
        fields = ['id', 'data', 'source', 'status']
        read_only_fields = ['id', 'source', 'status']

    def get_source(self, obj):
        source = obj.source.to_child()
        serializer = get_source_serializer(source.type)
        return serializer(source).data

    def validate(self, attrs):
        if self.instance:
            _validate_attrs(self.instance.campaign, attrs)
        return super().validate(attrs)

    def create(self, validated_data):
        raise NotSupported()


class DocumentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'data', 'campaign', 'status']
        read_only_fields = ['id', 'status']

    def validate(self, attrs):
        _validate_attrs(attrs.get('campaign'), attrs)
        return super().validate(attrs)

    def update(self, instance, validated_data):
        raise NotSupported()
