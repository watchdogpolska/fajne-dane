from rest_framework import serializers

from users.exceptions import PasswordsNotMatch, UsernameUsed
from users.models.user import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')
        read_only_fields = ['id']


class UserRegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    password1 = serializers.CharField(required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(required=True, style={'input_type': 'password'})

    def validate(self, attrs):
        if attrs['password1'] != attrs['password2']:
            raise PasswordsNotMatch()
        return super().validate(attrs)

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password1'],
        )
        user.save()
        return user

    def update(self, instance, validated_data):
        raise NotImplemented
