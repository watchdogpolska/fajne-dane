from typing import Dict

from rest_framework import serializers

from users.exceptions import PasswordsNotMatch, ActivationNotFound
from users.models import ActivationToken
from users.models.user import User


class PasswordResetSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)
    password = serializers.CharField(
        write_only=True, required=True, style={'input_type': 'password'})
    password_confirmation = serializers.CharField(
        write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        key_fields = ("token", )

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirmation']:
            raise PasswordsNotMatch()
        return super().validate(attrs)

    def update(self, instance: User, validated_data: Dict):
        instance.set_password(validated_data['password'])
        instance.save()
        return instance

    def retrieve(self) -> ActivationToken:
        token = ActivationToken.objects.filter(token=self.validated_data['token']).first()
        if not token:
            raise ActivationNotFound()
        return token


class PasswordChangeSerializer(serializers.Serializer):

    password = serializers.CharField(
        write_only=True, required=True, style={'input_type': 'password'})
    password_confirmation = serializers.CharField(
        write_only=True, required=True, style={'input_type': 'password'})

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirmation']:
            raise PasswordsNotMatch()
        return super().validate(attrs)

    def create(self, validated_data):
        raise NotImplemented()

    def update(self, instance: User, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()
        return instance
