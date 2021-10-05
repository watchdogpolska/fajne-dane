from rest_framework import serializers

from campaigns.models import Source


class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = ['id', 'name', ]
