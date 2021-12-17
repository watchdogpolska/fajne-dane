from rest_framework import serializers

from fajne_dane.core.serializers import ReadOnlySerializer
from .validation import ValidationErrorSerializer



class DocumentErrorSerializer(ReadOnlySerializer):
    index = serializers.IntegerField()
    data = serializers.JSONField()
    errors = ValidationErrorSerializer(many=True)


class DocumentFactoryReportSerializer(ReadOnlySerializer):
    is_valid = serializers.BooleanField()
    errors = DocumentErrorSerializer(many=True)
    documents_count = serializers.IntegerField()
