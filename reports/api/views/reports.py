from rest_framework import generics

from fajne_dane.core import IsAdminOrReadOnly
from reports.models import Report
from reports.serializers.report import ReportFullSerializer, ReportSerializer, ReportDetailsSerializer


class ReportList(generics.ListCreateAPIView):
    permission_classes = (IsAdminOrReadOnly,)
    queryset = Report.objects.all()
    serializer_class = ReportSerializer


class ReportDetails(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAdminOrReadOnly,)
    queryset = Report.objects.all()
    serializer_class = ReportDetailsSerializer


class ReportRender(generics.RetrieveAPIView):
    permission_classes = (IsAdminOrReadOnly,)
    queryset = Report.objects.all()
    serializer_class = ReportFullSerializer
