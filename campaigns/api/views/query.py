from rest_framework import generics

from campaigns.serializers import QuerySerializer
from campaigns.models import Query
from fajne_dane.core import IsAdminOrReadOnly


class QueryList(generics.ListAPIView):
    serializer_class = QuerySerializer
    permission_classes = (IsAdminOrReadOnly,)

    def get_queryset(self):
        campaign_id = self.kwargs.get("campaign_id")
        return Query.objects.filter(campaign_id=campaign_id)


class QueryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Query.objects.all()
    serializer_class = QuerySerializer
    permission_classes = (IsAdminOrReadOnly,)
