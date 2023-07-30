from rest_framework import serializers

from fajne_dane.core import RetrieveModelSerializer
from users.models.activation_token import ActivationToken


class ActivationTokenSerializer(RetrieveModelSerializer):
    token = serializers.CharField(required=True)

    class Meta:
        model = ActivationToken
