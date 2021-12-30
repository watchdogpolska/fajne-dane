from rest_framework import serializers

from fajne_dane.core.serializers import ReadOnlySerializer


class ValidationErrorSerializer(ReadOnlySerializer):
    code = serializers.CharField()
    message = serializers.CharField()


class ValidationReportSerializer(ReadOnlySerializer):
    is_valid = serializers.BooleanField()
    errors = ValidationErrorSerializer(many=True)
