from rest_framework import serializers

from reports.models.components import ReferencesComponent


class ReferencesComponentSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReferencesComponent
        fields = ['id', 'name', 'type', 'data', 'metadata']
        read_only_fields = ['id', 'type']
