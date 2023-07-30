from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status, views
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from campaigns.api.exceptions import FileSourceNotProcess
from campaigns.models import FileSource, Document, Campaign
from campaigns.models.consts import FileSourceStatus
from campaigns.models.sources.utils import load_data_frame
from campaigns.parsers.campaign_dataset_parser import CampaignDatasetParser
from campaigns.serializers import ParsingReportSerializer, \
    ParsingValidationReportSerializer
from campaigns.serializers.sources import FileSourceSerializer, FileSourceCreateSerializer, FileSourceContentSerializer


class FileSourceList(generics.ListAPIView):
    serializer_class = FileSourceSerializer
    permission_classes = (IsAdminUser,)

    def get_queryset(self):
        campaign_id = self.kwargs.get("campaign_id")
        return FileSource.objects.filter(campaign_id=campaign_id)


class FileSourceDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FileSourceSerializer
    permission_classes = (IsAdminUser,)
    queryset = FileSource


    def delete(self, request, *args, **kwargs):
        Document.objects.filter(source_id=kwargs['pk']).delete()
        return super().delete(request, *args, **kwargs)


class FileSourceCreate(generics.CreateAPIView):
    serializer_class = FileSourceCreateSerializer
    permission_classes = (IsAdminUser,)

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="Report created after parsing the provided file.",
                schema=ParsingValidationReportSerializer
            )
        }
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        instance = serializer.save(campaign_id=self.kwargs['campaign_id'])

        report = instance.validate_file()
        output_serializer = ParsingValidationReportSerializer(report)
        headers = self.get_success_headers(output_serializer.data)

        return (
            Response(
                output_serializer.data,
                status=status.HTTP_201_CREATED,
                headers=headers,
            )
            if report.is_valid
            else Response(
                output_serializer.data,
                status=status.HTTP_400_BAD_REQUEST,
                headers=headers,
            )
        )



class FileSourceValidate(views.APIView):
    permission_classes = (IsAdminUser,)
    serializer_class = ParsingReportSerializer

    def post(self, request, campaign_id):
        input_serializer = FileSourceContentSerializer(data=request.data)
        if input_serializer.is_valid():
            campaign = Campaign.objects.get(id=campaign_id)
            file = input_serializer.validated_data['file']
            df = load_data_frame(file)
            report = CampaignDatasetParser(campaign).validate(df)
            serializer = self.serializer_class(data=report.to_json())
            serializer.is_valid()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(input_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FileSourceReport(views.APIView):
    permission_classes = (IsAdminUser,)
    serializer_class = ParsingReportSerializer

    def get(self, request, pk):
        if file_source := FileSource.objects.filter(id=pk).first():
            if file_source.status in [FileSourceStatus.FAILED, FileSourceStatus.FINISHED]:
                return Response(file_source.raw_report, status=status.HTTP_200_OK)
            else:
                raise FileSourceNotProcess()
        return Response(status=status.HTTP_404_NOT_FOUND)
