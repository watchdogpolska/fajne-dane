from rest_framework import serializers

from users.models.activation_token import ActivationToken


class ActivationTokenSerializer(serializers.ModelSerializer):

    class Meta:
        model = ActivationToken
        fields = ('user', 'token', 'token_used', 'action_type', 'account_type')
        read_only_fields = fields
