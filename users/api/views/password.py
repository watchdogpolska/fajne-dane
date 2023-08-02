from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from fajne_dane.consts import Platform
from users.exceptions import EmailNotFound
from users.serializers import PasswordResetSerializer, UserEmailSerializer, PasswordChangeSerializer


class PasswordResetRequest(generics.GenericAPIView):
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
            user.send_reset_password_email(platform=platform)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordReset(generics.GenericAPIView):
    serializer_class = PasswordResetSerializer
    permission_classes = (AllowAny,)
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            token = serializer.retrieve()
            serializer.update(token.user, serializer.validated_data)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordChange(generics.GenericAPIView):
    serializer_class = PasswordChangeSerializer
    permission_classes = (AllowAny,)
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.update(request.user, serializer.validated_data)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
