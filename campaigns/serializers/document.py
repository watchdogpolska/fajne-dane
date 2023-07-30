from typing import Dict

from rest_framework import serializers

from campaigns.models import Document, Campaign
from campaigns.models.dto import DocumentDTO
from campaigns.serializers.institutions import InstitutionMinimalSerializer
from campaigns.serializers.document_query import DocumentQuerySerializer
from campaigns.serializers.sources import SourceSerializer
from campaigns.serializers.sources.utils import get_source_serializer
from fajne_dane.core.serializers import (
    ReadCreateModelSerializer, ReadUpdateModelSerializer, ReadOnlyModelSerializer
)


def _validate_attrs(campaign: Campaign, attrs: Dict):
    if 'data' in attrs:
        document_dto = DocumentDTO(data=attrs['data'], institution=None)
        campaign.validate_document(document_dto)


class DocumentSerializer(ReadUpdateModelSerializer):
    source = SourceSerializer()
    institution = InstitutionMinimalSerializer(read_only=True)

    class Meta:
        model = Document
        fields = ['id', 'source', 'status', 'institution', 'created', 'data']
        read_only_fields = ['id', 'source', 'status', 'institution', 'created', 'data']

    def validate(self, attrs):
        if self.instance:
            _validate_attrs(self.instance.campaign, attrs)
        return super().validate(attrs)


class DocumentFullSerializer(ReadUpdateModelSerializer):
    source = serializers.SerializerMethodField()
    document_queries = DocumentQuerySerializer(many=True, read_only=True)
    institution = InstitutionMinimalSerializer(read_only=True)

    class Meta:
        model = Document
        fields = ['id', 'data', 'source', 'status', 'institution', 'created', 'document_queries']
        read_only_fields = ['id', 'source', 'status', 'institution', 'created', 'document_queries']

    def get_source(self, obj):
        source = obj.source.to_child()
        serializer = get_source_serializer(source.type)
        return serializer(source).data

    def validate(self, attrs):
        if self.instance:
            _validate_attrs(self.instance.campaign, attrs)
        return super().validate(attrs)


class DocumentCreateSerializer(ReadCreateModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'data', 'campaign', 'status', 'institution']
        read_only_fields = ['id', 'status']

    def validate(self, attrs):
        _validate_attrs(attrs.get('campaign'), attrs)
        return super().validate(attrs)


class DocumentIdSerializer(ReadOnlyModelSerializer):
    class Meta:
        model = Document
        fields = ['id']
