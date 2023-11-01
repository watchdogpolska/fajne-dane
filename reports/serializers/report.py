from typing import List

from rest_framework import serializers

from fajne_dane.core.serializers import (
    ReadCreateModelSerializer,
    ReadOnlyModelSerializer,
)
from reports.models import Report
from reports.models.components import ReportComponent
from reports.serializers.components import get_report_component_serializer


class ReportSerializer(ReadCreateModelSerializer):
    class Meta:
        model = Report
        fields = ['id', 'name']


class ReportFullSerializer(ReadOnlyModelSerializer):
    components = serializers.SerializerMethodField()
    class Meta:
        model = Report
        fields = ['id', 'name', 'components']
        read_only_fields = ['id', 'name', 'components']

    def get_components(self, obj) -> List[ReportComponent]:
        results = []
        for raw_component in obj.components.all():
            component = raw_component.to_child()
            serializer = get_report_component_serializer(component.type)
            results.append(serializer(component).data)
        return results
