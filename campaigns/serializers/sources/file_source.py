from rest_framework import serializers

from campaigns.models import FileSource
from fajne_dane.core.serializers import (
    ReadOnlySerializer, ReadUpdateModelSerializer, ReadCreateModelSerializer, ReadOnlyModelSerializer
)


class FileSourceSerializer(ReadUpdateModelSerializer):
    class Meta:
        model = FileSource
        fields = ['id', 'name', 'description', 'file', 'source_link', 'source_date', 'created', 'type', 'status']
        read_only_fields = ['id', 'file', 'created', 'type', 'status']

        extra_kwargs = {
            'file': {'required': False},
        }


class FileSourceMinimalSerializer(ReadOnlyModelSerializer):
    class Meta:
        model = FileSource
        fields = ['id', 'name', 'type']
        read_only_fields = ['id', 'name', 'type']


class FileSourceCreateSerializer(ReadCreateModelSerializer):
    class Meta:
        model = FileSource
        fields = ['id', 'name', 'description', 'file', 'source_link', 'source_date']
        read_only_fields = ['id']


class FileSourceContentSerializer(ReadOnlySerializer):
    file = serializers.FileField()
