from campaigns.models import Campaign
from .document_data_field import DocumentDataFieldCreateSerializer
from fajne_dane.core.serializers import ReadUpdateModelSerializer, ReadCreateModelSerializer


class CampaignSerializer(ReadUpdateModelSerializer):
    class Meta:
        model = Campaign
        fields = ['id', 'name', 'status', 'created']
        read_only_fields = ['id', 'status', 'created']


class CampaignFullSerializer(ReadUpdateModelSerializer):
    document_fields_objects = DocumentDataFieldCreateSerializer(many=True, read_only=True)
    
    class Meta:
        model = Campaign
        fields = ['id', 'name', 'status', 'created', 'template', 'document_fields_objects']
        read_only_fields = ['id', 'status', 'created', 'template', 'document_fields_objects']


class CampaignCreateSerializer(ReadCreateModelSerializer):
    class Meta:
        model = Campaign
        fields = ['id', 'name', 'template', 'status']

    def create(self, validated_data):
        from campaigns.models.factory import campaign_factory
        return campaign_factory.create(validated_data['name'], validated_data['template'])
