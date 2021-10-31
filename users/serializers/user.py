from rest_framework import serializers

from lib.serializers.retrieve_model_serializer import RetrieveModelSerializer
from users.exceptions import PasswordsNotMatch, EmailUsed
from users.models.user import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email')
        read_only_fields = ['id']


class UserRegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    password = serializers.CharField(
        write_only=True, required=True, style={'input_type': 'password'})
    password_confirmation = serializers.CharField(
        write_only=True, required=True, style={'input_type': 'password'})

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirmation']:
            raise PasswordsNotMatch()
        if User.objects.filter(email=attrs['email']).first():
            raise EmailUsed()
        return super().validate(attrs)

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password'],
        )
        user.save()
        return user

    def update(self, instance, validated_data):
        raise NotImplemented


class UserEmailSerializer(RetrieveModelSerializer):

    class Meta:
        model = User
        fields = ("email",)
