from campaigns.models import Campaign
from .document_data_field import DocumentDataFieldCreateSerializer
from fajne_dane.core.serializers import ReadUpdateModelSerializer, ReadCreateModelSerializer
from .institutions.institution_group import InstitutionGroupMinimalSerializer


class CampaignSerializer(ReadUpdateModelSerializer):
    institution_group = InstitutionGroupMinimalSerializer(read_only=True)
    class Meta:
        model = Campaign
        fields = ['id', 'name', 'status', 'created', 'institution_group']
        read_only_fields = ['id', 'status', 'created', 'institution_group']


class CampaignFullSerializer(ReadUpdateModelSerializer):
    document_fields_objects = DocumentDataFieldCreateSerializer(many=True, read_only=True)
    institution_group = InstitutionGroupMinimalSerializer(read_only=True)

    class Meta:
        model = Campaign
        fields = ['id', 'name', 'status', 'created', 'template', 'institution_group', 'document_fields_objects']
        read_only_fields = ['id', 'status', 'created', 'template', 'institution_group', 'document_fields_objects']


class CampaignCreateSerializer(ReadCreateModelSerializer):
    class Meta:
        model = Campaign
        fields = ['id', 'name', 'template', 'status', 'institution_group']

    def create(self, validated_data):
        from campaigns.models.factory import campaign_factory
        return campaign_factory.create(
            name=validated_data['name'],
            institution_group=validated_data['institution_group'],
            template=validated_data['template']
        )
