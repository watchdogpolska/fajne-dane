from rest_framework import generics, status
from rest_framework.response import Response

from fajne_dane.core import IsAdminOrReadOnly
from reports.models import ReportComponent
from reports.serializers.components import get_report_component_serializer


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
            print(component.id)
            print(report.layout)
            if str(component.id) in report.layout:
                del report.layout[str(component.id)]
                print("USUWANKO")
                report.save()
            component.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

