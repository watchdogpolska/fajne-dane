from rest_framework import serializers

from campaigns.models.document_data_field import DocumentDataField


class DocumentDataFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentDataField
        fields = ['name', 'widget', 'type']
