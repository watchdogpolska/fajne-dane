from rest_framework import serializers

from fajne_dane.core.serializers import ReadOnlySerializer


class IdListSerializer(ReadOnlySerializer):
    ids = serializers.ListField(
       child=serializers.IntegerField()
    )
