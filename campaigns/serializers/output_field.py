from rest_framework import serializers
from campaigns.models import OutputField
from fajne_dane.core.exceptions import NotSupported


class OutputFieldSerializer(serializers.ModelSerializer):

    class Meta:
        model = OutputField
        fields = ('id', 'name', 'widget', 'answers', 'metadata', 'type', 'validation', 'default_answer')
        read_only_fields = ['id']

    def update(self, instance, validated_data):
        raise NotSupported()
