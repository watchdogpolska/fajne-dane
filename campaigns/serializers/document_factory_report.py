from rest_framework import serializers

from fajne_dane.core.exceptions import NotSupported


class ParsingErrorSerializer(serializers.Serializer):
    code = serializers.CharField()
    message = serializers.CharField()

    def update(self, instance, validated_data):
        raise NotSupported()

    def create(self, validated_data):
        raise NotSupported()



class DocumentErrorSerializer(serializers.Serializer):
    index = serializers.IntegerField()
    data = serializers.JSONField()
    errors = ParsingErrorSerializer(many=True)

    def update(self, instance, validated_data):
        raise NotSupported()

    def create(self, validated_data):
        raise NotSupported()


class DocumentFactoryReportSerializer(serializers.Serializer):
    is_valid = serializers.BooleanField()
    errors = DocumentErrorSerializer(many=True)
    documents_count = serializers.IntegerField()

    def update(self, instance, validated_data):
        raise NotSupported()

    def create(self, validated_data):
        raise NotSupported()
