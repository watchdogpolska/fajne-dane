from rest_framework import serializers
from fajne_dane.core.serializers import ReadOnlySerializer


class TemplateContentSerializer(ReadOnlySerializer):
    template = serializers.JSONField()
