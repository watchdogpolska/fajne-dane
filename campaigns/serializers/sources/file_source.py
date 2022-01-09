from rest_framework import serializers

from campaigns.models import FileSource
from fajne_dane.core.serializers import (
    ReadOnlySerializer, ReadUpdateOnlyModelSerializer, ReadCreateOnlyModelSerializer, ReadOnlyModelSerializer
)


class FileSourceSerializer(ReadUpdateOnlyModelSerializer):
    class Meta:
        model = FileSource
        fields = ['id', 'name', 'description', 'file', 'source_link', 'source_date', 'created', 'type']
        read_only_field = ['id', 'file', 'created', 'type']

        extra_kwargs = {
            'file': {'required': False},
        }


class FileSourceMinimalSerializer(ReadOnlyModelSerializer):
    class Meta:
        model = FileSource
        fields = ['id', 'name', 'type']
        read_only_field = ['id', 'name', 'type']


class FileSourceCreateSerializer(ReadCreateOnlyModelSerializer):
    class Meta:
        model = FileSource
        fields = ['id', 'name', 'description', 'file', 'source_link', 'source_date']
        read_only_field = ['id']


class FileSourceContentSerializer(ReadOnlySerializer):
    file = serializers.FileField()
