from rest_framework import serializers

from reports.models.components import HTMLComponent


class HTMLComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = HTMLComponent
        fields = ['id', 'name', 'type', 'text']
        read_only_fields = ['id', 'type']
