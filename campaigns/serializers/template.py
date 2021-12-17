from rest_framework import serializers
from campaigns.serializers import ValidationErrorSerializer
from fajne_dane.core.serializers import ReadOnlySerializer


class TemplateInfoSerializer(ReadOnlySerializer):
    template = serializers.JSONField()


class TemplateValidationReportSerializer(ReadOnlySerializer):
    is_valid = serializers.BooleanField()
    errors = ValidationErrorSerializer(many=True)
