from rest_framework import status, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from campaigns.serializers import (
    TemplateInfoSerializer, TemplateValidationReportSerializer
)
from campaigns.validators.template import CAMPAIGN_SCHEMA, prepare_validation_report


class GetMetaTemplate(views.APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = TemplateInfoSerializer

    def get(self, request):
        serializer = self.serializer_class(data={"template": CAMPAIGN_SCHEMA})
        serializer.is_valid()
        return Response(serializer.data, status=status.HTTP_200_OK)


class ValidateCampaignTemplate(views.APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = TemplateValidationReportSerializer

    def post(self, request):
        input_serializer = TemplateInfoSerializer(data=request.data)
        if input_serializer.is_valid():
            report = prepare_validation_report(input_serializer.data['template'])
            serializer = self.serializer_class(data=report.to_json())
            serializer.is_valid()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(input_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
