from rest_framework import serializers

from campaigns.models import Source
from fajne_dane.core.exceptions import NotSupported


class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = ['id', 'name']

    def update(self, instance, validated_data):
        raise NotSupported()

    def create(self, validated_data):
        raise NotSupported()
