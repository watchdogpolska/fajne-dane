from rest_framework import serializers
from rest_framework.authtoken.admin import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')
        read_only_fields = ['id']


class UserRegistrationSerializer(serializers.Serializer):

    username = serializers.CharField()
    email = serializers.EmailField(required=True)
    password1 = serializers.CharField(style={'input_type': 'password'})
    password2 = serializers.CharField(style={'input_type': 'password'})

    def create(self, validated_data):
        ...

    def update(self, instance, validated_data):
        pass
