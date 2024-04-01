from rest_framework import serializers

from fajne_dane.core.serializers import (
    ReadOnlyModelSerializer,
)
from reports.models import DataSource


class DataSourceSerializer(ReadOnlyModelSerializer):
    campaign_name = serializers.SerializerMethodField()
    file_url = serializers.SerializerMethodField()
    
    class Meta:
        model = DataSource
        fields = ['id', 'campaign_name', 'file_url']
        read_only_fields = ['id', 'campaign_name', 'file_url']

    def get_campaign_name(self, obj):
        return obj.campaign.name

    def get_file_url(self, obj):
        return obj.file.url


class DataSourceFullSerializer(DataSourceSerializer):
    class Meta:
        model = DataSource
        fields = ['id', 'campaign_name', 'file_url', 'query_labels', 'available_keys']
        read_only_fields = ['id', 'campaign_name', 'file_url', 'query_labels', 'available_keys']
