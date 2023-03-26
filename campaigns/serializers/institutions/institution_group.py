from campaigns.models import InstitutionGroup
from fajne_dane.core.serializers import (
    ReadOnlyModelSerializer, ReadCreateModelSerializer, ReadUpdateModelSerializer
)


class InstitutionGroupSerializer(ReadOnlyModelSerializer):
    class Meta:
        model = InstitutionGroup
        fields = ["id", "parent_id", "name", "institutions_count"]


class InstitutionGroupDetailsSerializer(ReadUpdateModelSerializer):
    class Meta:
        model = InstitutionGroup
        fields = ["id", "name", "fields", "institutions_count"]


class InstitutionGroupCreateSerializer(ReadCreateModelSerializer):
    class Meta:
        model = InstitutionGroup
        fields = ["id", "parent_id", "name", "fields"]

