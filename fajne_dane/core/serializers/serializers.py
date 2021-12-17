from rest_framework import serializers
from fajne_dane.core.exceptions import NotSupported


class ReadOnlySerializer(serializers.Serializer):

    def update(self, instance, validated_data):
        raise NotSupported()

    def create(self, validated_data):
        raise NotSupported()


class ReadCreateOnlySerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        raise NotSupported()

    def create(self, validated_data):
        return super().create(validated_data)


class ReadUpdateOnlySerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

    def create(self, validated_data):
        raise NotSupported()


class ReadOnlyModelSerializer(serializers.ModelSerializer):

    def update(self, instance, validated_data):
        raise NotSupported()

    def create(self, validated_data):
        raise NotSupported()


class ReadCreateOnlyModelSerializer(serializers.ModelSerializer):
    def update(self, instance, validated_data):
        raise NotSupported()

    def create(self, validated_data):
        return super().create(validated_data)


class ReadUpdateOnlyModelSerializer(serializers.ModelSerializer):
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

    def create(self, validated_data):
        raise NotSupported()
