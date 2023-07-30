from campaigns.models.document_data_field import DocumentDataField
from fajne_dane.core.exceptions import NotSupported
from fajne_dane.core.serializers import ReadCreateModelSerializer


class DocumentDataFieldCreateSerializer(ReadCreateModelSerializer):
    class Meta:
        model = DocumentDataField
        fields = ['id', 'name', 'widget', 'type']
        read_only_fields = ['id']

    def update(self, instance, validated_data):
        raise NotSupported()
