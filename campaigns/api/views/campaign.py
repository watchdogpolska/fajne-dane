from rest_framework import generics

from campaigns.models import Campaign
from campaigns.serializers import (
    CampaignSerializer, CampaignCreateSerializer, CampaignFullSerializer
)


class CampaignList(generics.ListAPIView):
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer


class CampaignDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Campaign.objects.all()
    serializer_class = CampaignFullSerializer


class CampaignCreate(generics.CreateAPIView):
    queryset = Campaign.objects.all()
    serializer_class = CampaignCreateSerializer
