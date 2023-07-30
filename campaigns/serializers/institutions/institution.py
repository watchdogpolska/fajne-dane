from campaigns.models import Institution
from fajne_dane.core.serializers import (
    ReadOnlyModelSerializer, ReadUpdateModelSerializer, ReadCreateModelSerializer
)


class InstitutionMinimalSerializer(ReadOnlyModelSerializer):
    class Meta:
        model = Institution
        fields = ["id", "key", "name"]


class InstitutionDataSerializer(ReadOnlyModelSerializer):
    class Meta:
        model = Institution
        fields = ["id", "key", "name", "link", "address"]


class InstitutionSerializer(ReadOnlyModelSerializer):
    parent = InstitutionMinimalSerializer(read_only=True)
    class Meta:
        model = Institution
        fields = ["id", "parent", "key", "name", "link"]


class InstitutionDetailsSerializer(ReadUpdateModelSerializer):
    class Meta:
        model = Institution
        fields = ["id", "group_id", "key", "name", "link", "address"]


class InstitutionCreateSerializer(ReadCreateModelSerializer):
    class Meta:
        model = Institution
        fields = ["id", "group_id", "parent_id", "key", "name", "link", "address"]
