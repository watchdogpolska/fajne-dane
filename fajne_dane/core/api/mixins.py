from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework import status


class TwoTypeCreateModelMixin:
    """
    Create a model instance.
    """
    def create(self, request, *args, **kwargs):
        deserializer = self.get_input_serializer(data=request.data)
        deserializer.is_valid(raise_exception=True)
        output = self.perform_create(deserializer)

        serializer = self.get_output_serializer(output)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save()

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}
