from rest_framework import serializers

from campaigns.models import UserSource
from fajne_dane.core.exceptions import NotSupported
from users.serializers import UserSerializer


class UserSourceSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserSource
        fields = ['id', 'name', 'user']
        read_only_field = ['id', 'user']

    def update(self, instance, validated_data):
        raise NotSupported()

    def create(self, validated_data):
        raise NotSupported()
