from rest_framework import generics, status
from rest_framework.response import Response

from fajne_dane.core import IsAdminOrReadOnly
from reports.models import Report
from reports.models.components import ReportComponentTypes
from reports.serializers.components.header import HeaderComponentSerializer


class HeaderComponentCreate(generics.CreateAPIView):
    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = HeaderComponentSerializer

    def create(self, request, report_id, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            report = Report.objects.get(id=report_id)
            instance = serializer.save(report=report, type=ReportComponentTypes.HEADER)

            report.layout[str(instance.id)] = {"order": report.components.count(), "width": 6}
            report.save()

            output_serializer = self.get_serializer(instance)
            headers = self.get_success_headers(output_serializer.data)

            return Response(output_serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
