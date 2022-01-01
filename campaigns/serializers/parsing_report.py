from rest_framework import serializers

from fajne_dane.core.serializers import ReadOnlySerializer
from .validation import ValidationErrorSerializer


class DocumentParsingReportSerializer(ReadOnlySerializer):
    index = serializers.IntegerField()
    data = serializers.JSONField()
    errors = ValidationErrorSerializer(many=True)


class ParsingReportSerializer(ReadOnlySerializer):
    is_valid = serializers.BooleanField()
    file_errors = ValidationErrorSerializer(many=True)
    documents_errors = DocumentParsingReportSerializer(many=True)
    valid_documents_count = serializers.IntegerField()
    invalid_documents_count = serializers.IntegerField()
