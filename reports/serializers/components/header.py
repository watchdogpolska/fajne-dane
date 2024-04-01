from rest_framework import serializers

from reports.models.components import HeaderComponent


class HeaderComponentSerializer(serializers.ModelSerializer):

    class Meta:
        model = HeaderComponent
        fields = ['id', 'name', 'type', 'title', 'subtitle']
        read_only_fields = ['id', 'type']
