from rest_framework import generics, status, views
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response

from campaigns.models.dto import DocumentDTO
from campaigns.models.factory.documents_factory import DocumentsFactory
from campaigns.serializers import DocumentSerializer, DocumentCreateSerializer, DocumentFullSerializer, IdListSerializer
from campaigns.models import Document, UserSource, Institution, Campaign


class DocumentList(generics.ListAPIView):
    serializer_class = DocumentSerializer
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

        campaign = Campaign.objects.get(id=self.kwargs['campaign_id'])
        source, _ = UserSource.objects.get_or_create(user=request.user)

        dto = DocumentDTO(data=serializer.validated_data['data'])

        factory = DocumentsFactory(campaign=campaign, source=source)
        document = factory.create(dto)

        serializer = self.get_serializer(document)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class DocumentBulkDelete(views.APIView):
    permission_classes = (IsAdminUser,)
    serializer_class = IdListSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            documents = Document.objects.filter(id__in=serializer.validated_data['ids'])
            documents.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
