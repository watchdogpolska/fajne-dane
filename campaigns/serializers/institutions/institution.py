from campaigns.models import Institution
from fajne_dane.core.serializers import ReadOnlyModelSerializer


class InstitutionSerializer(ReadOnlyModelSerializer):
    class Meta:
        model = Institution
        fields = ['id', 'key', 'name', "link", "address"]
