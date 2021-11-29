from rest_framework import serializers
from campaigns.models import Campaign
from fajne_dane.core.exceptions import NotSupported


class CampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = ['id', 'name', 'status', 'created']
        read_only_fields = ['id', 'status', 'created']

    def create(self, validated_data):
        raise NotSupported()


class CampaignCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = ['id', 'name', 'template', 'status']

    def update(self, instance, validated_data):
        raise NotSupported()
