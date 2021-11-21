from rest_framework import serializers

from campaigns.models import FileSource
from fajne_dane.core.exceptions import NotSupported


class FileSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileSource
        fields = ['id', 'name', 'description', 'file']
        read_only_field = ['id', 'file']

        extra_kwargs = {
            'file': {'required': False},
        }

    def create(self, validated_data):
        raise NotSupported()


class FileSourceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileSource
        fields = ['id', 'name', 'description', 'file']
        read_only_field = ['id']

    def update(self, instance, validated_data):
        raise NotSupported()
