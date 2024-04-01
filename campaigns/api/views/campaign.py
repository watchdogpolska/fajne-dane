from rest_framework import generics

from campaigns.serializers import (
    CampaignSerializer, CampaignCreateSerializer, CampaignFullSerializer
)
from campaigns.models import Campaign
from fajne_dane.core import IsAdminOrReadOnly


class CampaignList(generics.ListAPIView):
    permission_classes = (IsAdminOrReadOnly,)
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer


class CampaignDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAdminOrReadOnly,)
    queryset = Campaign.objects.all()
    serializer_class = CampaignFullSerializer


class CampaignCreate(generics.CreateAPIView):
    permission_classes = (IsAdminOrReadOnly,)
    queryset = Campaign.objects.all()
    serializer_class = CampaignCreateSerializer
