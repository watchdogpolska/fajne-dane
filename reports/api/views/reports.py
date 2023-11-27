from rest_framework import generics
from rest_framework.permissions import AllowAny

from reports.models import Report
from reports.serializers.report import ReportFullSerializer, ReportSerializer, ReportDetailsSerializer


class ReportList(generics.ListAPIView):
    permission_classes = (AllowAny,)
    queryset = Report.objects.all()
    serializer_class = ReportSerializer


class ReportDetails(generics.RetrieveUpdateAPIView):
    permission_classes = (AllowAny,)
    queryset = Report.objects.all()
    serializer_class = ReportDetailsSerializer


class ReportRender(generics.RetrieveAPIView):
    permission_classes = (AllowAny,)
    queryset = Report.objects.all()
    serializer_class = ReportFullSerializer
