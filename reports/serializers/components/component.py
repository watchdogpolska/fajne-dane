from rest_framework import serializers

from reports.models.components import ReportComponent


class ReportComponentSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReportComponent
        fields = ['id', 'name', 'type', 'metadata']
