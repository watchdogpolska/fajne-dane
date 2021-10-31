from rest_framework import generics, status
from rest_framework import mixins
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from users.models import ActivationToken
from users.serializers.activation_token import ActivationTokenSerializer
from users.serializers.user import UserRegistrationSerializer, UserSerializer, UserEmailSerializer


class UserRegistration(mixins.CreateModelMixin,
                       generics.GenericAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny,)
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class AccountActivation(generics.GenericAPIView):
    serializer_class = ActivationTokenSerializer
    permission_classes = (AllowAny,)
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            token = serializer.retrieve()
            token.activate()
        return Response(status=status.HTTP_200_OK)


class TokenReactivation(generics.GenericAPIView):
    serializer_class = UserEmailSerializer
    permission_classes = (AllowAny,)
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.retrieve()
            token.activate()
        return Response(status=status.HTTP_200_OK)
