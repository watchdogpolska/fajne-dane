from campaigns.models import InstitutionGroup
from fajne_dane.core.serializers import (
    ReadOnlyModelSerializer, ReadCreateModelSerializer, ReadUpdateModelSerializer
)


class InstitutionGroupSerializer(ReadOnlyModelSerializer):
    class Meta:
        model = InstitutionGroup
        fields = ["id", "parent_id", "name", "institutions_count"]


class InstitutionGroupMinimalSerializer(ReadOnlyModelSerializer):
    class Meta:
        model = InstitutionGroup
        fields = ["id", "name"]


class InstitutionGroupDetailsSerializer(ReadUpdateModelSerializer):
    parent = InstitutionGroupMinimalSerializer(read_only=True)
    class Meta:
        model = InstitutionGroup
        fields = ["id", "name", "fields", "institutions_count", "parent"]


class InstitutionGroupCreateSerializer(ReadCreateModelSerializer):
    class Meta:
        model = InstitutionGroup
        fields = ["id", "parent_id", "name", "fields"]

