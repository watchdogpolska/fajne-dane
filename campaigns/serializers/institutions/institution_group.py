from campaigns.models import InstitutionGroup
from fajne_dane.core.serializers import ReadOnlyModelSerializer


class InstitutionGroupSerializer(ReadOnlyModelSerializer):
    class Meta:
        model = InstitutionGroup
        fields = ['id', 'name', "institutions_count"]
