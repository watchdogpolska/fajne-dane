from django.contrib.auth import login, logout
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from users.exceptions import (
    PasswordIncorrect, EmailNotFound, UnableToAuthenticate, AccountInactive
)
from users.serializers import UserSerializer
from users.serializers.user import UserLoginSerializer


class Login(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = (AllowAny,)
    authentication_classes = []

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="Authenticated user",
                schema=UserSerializer
            )
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        try:
            if serializer.is_valid(raise_exception=True):
                user = serializer.retrieve()
                login(request, user)
                serializer = UserSerializer(user)
                return Response(serializer.data)
        except (PasswordIncorrect, EmailNotFound, AccountInactive):
            raise UnableToAuthenticate()


class Logout(generics.GenericAPIView):
    serializer_class = None

    @swagger_auto_schema(
        responses={
            status.HTTP_204_NO_CONTENT: openapi.Response(
                description="No content"
            )
        }
    )
    def get(self, request, *args, **kwargs):
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)
