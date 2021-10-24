from rest_framework import serializers
from campaigns.models import Document


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'data']
        read_only_fields = ['id']
