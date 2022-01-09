from campaigns.models import UserSource
from fajne_dane.core.serializers import ReadOnlyModelSerializer
from users.serializers import UserSerializer


class UserSourceSerializer(ReadOnlyModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserSource
        fields = ['id', 'user', 'type']
        read_only_field = ['id', 'user', 'type']
