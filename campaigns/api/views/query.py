from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAdminUser

from campaigns.serializers import QuerySerializer
from campaigns.models import Query


class QueryList(generics.ListAPIView):
    serializer_class = QuerySerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        campaign_id = self.kwargs.get("campaign_id")
        queries = Query.objects.filter(campaign_id=campaign_id)
        return queries


class QueryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Query.objects.all()
    serializer_class = QuerySerializer
    permission_classes = (IsAdminUser,)
