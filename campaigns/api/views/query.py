from rest_framework import generics

from campaigns.serializers import QuerySerializer
from campaigns.models import Query


class QueryList(generics.ListCreateAPIView):
    queryset = Query.objects.all()
    serializer_class = QuerySerializer


class QueryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Query.objects.all()
    serializer_class = QuerySerializer
