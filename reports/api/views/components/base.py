from rest_framework import generics, status
from rest_framework.response import Response

from fajne_dane.core import IsAdminOrReadOnly
from reports.models import Report
from reports.models import ReportComponent
from reports.models.components.data_component import DataComponent
from reports.models.data_views import get_data_view_class, DataViewTypes
from reports.serializers.components import get_report_component_serializer
from reports.serializers.data_view import DataViewCreateSerializer


class ReportComponentDetails(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAdminOrReadOnly,)

    def __init__(self, *args, **kwargs):
        self._component_object = None
        self._component_id = None
        super().__init__(*args, **kwargs)

    def get_component_object(self):
        component_id = self.request.parser_context['kwargs']['pk']
        current_id = getattr(self, '_component_id')
        if current_id != component_id:
            self._component_id = component_id
            self._component_object = ReportComponent.objects.get(id=component_id).to_child()
        return self._component_object

    def get_serializer_class(self):
        component = self.get_component_object()
        return get_report_component_serializer(component.type)

    def retrieve(self, request, pk, *args, **kwargs):
        component = self.get_component_object()
        serializer = self.get_serializer_class()
        _serializer = serializer(component)
        return Response(_serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk, *args, **kwargs):
        component = self.get_component_object()
        serializer = self.get_serializer_class()
        if request.method == 'PATCH':
            _serializer = serializer(component, data=request.data, partial=True)
        else:
            _serializer = serializer(component, data=request.data)
        if _serializer.is_valid():
            _serializer.update(component, _serializer.validated_data)
            component.refresh_from_db()
            _serializer = serializer(component)
            return Response(_serializer.data, status=status.HTTP_200_OK)
        return Response(_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk, *args, **kwargs):
        component = ReportComponent.objects.filter(id=pk).first()
        if component:
            report = component.report
            if str(component.id) in report.layout:
                del report.layout[str(component.id)]
                report.save()

            data_component = DataComponent.objects.filter(id=component.id).first()
            if data_component:
                data_component.data_view.delete()

            component.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class BaseComponentCreate(generics.CreateAPIView):
    permission_classes = (IsAdminOrReadOnly,)

    def create(self, request, report_id, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            report = Report.objects.get(id=report_id)
            instance = serializer.save(report=report)

            report.layout[str(instance.id)] = {"order": report.components.count(), "width": 6}
            report.save()

            output_serializer = self.get_serializer(instance)
            headers = self.get_success_headers(output_serializer.data)

            return Response(output_serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class BaseDataComponentCreate(generics.CreateAPIView):
    permission_classes = (IsAdminOrReadOnly,)

    def create(self, request, report_id, *args, **kwargs):
        report = Report.objects.get(id=report_id)
        data_view_serializer = DataViewCreateSerializer(data=request.data["data"])

        if data_view_serializer.is_valid():
            class_type = data_view_serializer.validated_data['type']
            data_view_class = get_data_view_class(DataViewTypes(class_type))
            data_view = data_view_class.objects.create(**data_view_serializer.validated_data)
            data_view.update()

            input_serializer = self.get_serializer(data=request.data["component"])
            input_serializer.is_valid(raise_exception=True)
            instance = input_serializer.save(data_view=data_view, report_id=report_id)

            report.layout[str(instance.id)] = {"order": report.components.count(), "width": 12}
            report.save()

            output_serializer = self.get_serializer(instance)
            headers = self.get_success_headers(output_serializer.data)
            return Response(output_serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(data_view_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
