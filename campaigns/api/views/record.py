from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response

from campaigns.serializers import RecordSerializer
from campaigns.models import Record, UserSource


class RecordList(generics.ListAPIView):
    serializer_class = RecordSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        doc_query_id = self.kwargs.get("doc_query_id")
        records = Record.objects.filter(parent_id=doc_query_id)
        return records


class RecordDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Record.objects.all()
    serializer_class = RecordSerializer
    permission_classes = (IsAdminUser,)


class RecordCreate(generics.CreateAPIView):
    serializer_class = RecordSerializer
    permission_classes = (IsAdminUser,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        source, _ = UserSource.objects.get_or_create(user=request.user)
        serializer.save(parent_id=self.kwargs['doc_query_id'], source_id=source.id)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
