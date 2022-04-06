from campaigns.models import Campaign
from .document_data_field import DocumentDataFieldCreateSerializer
from fajne_dane.core.serializers import ReadUpdateOnlyModelSerializer, ReadCreateOnlyModelSerializer


class CampaignSerializer(ReadUpdateOnlyModelSerializer):
    class Meta:
        model = Campaign
        fields = ['id', 'name', 'status', 'created']
        read_only_fields = ['id', 'status', 'created']


class CampaignFullSerializer(ReadUpdateOnlyModelSerializer):
    document_fields_objects = DocumentDataFieldCreateSerializer(many=True, read_only=True)
    
    class Meta:
        model = Campaign
        fields = ['id', 'name', 'status', 'created', 'template', 'document_fields_objects']
        read_only_fields = ['id', 'status', 'created', 'template', 'document_fields_objects']


class CampaignCreateSerializer(ReadCreateOnlyModelSerializer):
    class Meta:
        model = Campaign
        fields = ['id', 'name', 'template', 'status']

    def create(self, validated_data):
        from campaigns.models.factory import campaign_factory
        campaign = campaign_factory.create(validated_data['name'], validated_data['template'])
        return campaign
