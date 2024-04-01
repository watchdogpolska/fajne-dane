from rest_framework import generics, status
from rest_framework.response import Response

from fajne_dane.core import IsAdminOrReadOnly
from reports.models import Report
from reports.models.data_views import get_data_view_class, DataViewTypes
from reports.serializers.components.bar_plot import BarPlotComponentSerializer
from reports.serializers.data_view import DataViewCreateSerializer


class BarPlotComponentCreate(generics.CreateAPIView):
    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = BarPlotComponentSerializer

    def create(self, request, report_id, *args, **kwargs):
        report = Report.objects.get(id=report_id)
        data_view_serializer = DataViewCreateSerializer(data=request.data["data"])

        if data_view_serializer.is_valid():
            class_type = data_view_serializer.validated_data['type']
            data_view_class = get_data_view_class(DataViewTypes(class_type))
            data_view = data_view_class.objects.create(**data_view_serializer.validated_data)
            data_view.update()

            input_serializer = self.get_serializer(data=request.data["component"])

            instance = input_serializer.save(data_view=data_view, report_id=report_id)

            report.layout[str(instance.id)] = {"order": report.components.count(), "width": 12}
            report.save()

            output_serializer = self.get_serializer(instance)
            headers = self.get_success_headers(output_serializer.data)
            return Response(output_serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(data_view_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
