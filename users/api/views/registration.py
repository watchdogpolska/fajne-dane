from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework import mixins
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from fajne_dane.consts import Platform
from users.exceptions import EmailNotFound
from users.serializers.activation_token import ActivationTokenSerializer
from users.serializers.user import UserRegistrationSerializer, UserEmailSerializer


class UserRegister(mixins.CreateModelMixin, generics.GenericAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny,)
    authentication_classes = []

    def perform_create(self, serializer):
        """Creates a new User object and sends registration email."""
        super().perform_create(serializer)
        user = serializer.instance
        user.send_registration_email(platform=Platform.API)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class AccountActivate(generics.GenericAPIView):
    serializer_class = ActivationTokenSerializer
    permission_classes = (AllowAny,)
    authentication_classes = []

    @swagger_auto_schema(
        responses={
            status.HTTP_204_NO_CONTENT: openapi.Response(
                description="No content"
            )
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            token = serializer.retrieve()
            token.activate()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TokenReactivate(generics.GenericAPIView):
    serializer_class = UserEmailSerializer
    permission_classes = (AllowAny,)
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.retrieve()
            if not user:
                raise EmailNotFound()
            platform = request.GET.get("platform", Platform.API)
            user.send_registration_email(platform=platform)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
