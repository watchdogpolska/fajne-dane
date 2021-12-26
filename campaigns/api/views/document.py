from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response

from campaigns.serializers import DocumentSerializer, DocumentCreateSerializer, DocumentFullSerializer
from campaigns.models import Document, UserSource


class DocumentList(generics.ListAPIView):
    serializer_class = DocumentFullSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        campaign_id = self.kwargs.get("campaign_id")
        documents = Document.objects.filter(campaign_id=campaign_id)
        return documents


class DocumentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentFullSerializer
    permission_classes = (IsAdminUser,)


class DocumentCreate(generics.CreateAPIView):
    serializer_class = DocumentCreateSerializer
    permission_classes = (IsAdminUser,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        source, _ = UserSource.objects.get_or_create(user=request.user)
        serializer.save(campaign_id=self.kwargs['campaign_id'], source_id=source.id)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
