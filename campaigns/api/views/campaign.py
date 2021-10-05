from rest_framework import generics
from rest_framework.permissions import IsAdminUser

from campaigns.serializers import (
    CampaignSerializer, CampaignCreateSerializer
)
from campaigns.models import Campaign


class CampaignList(generics.ListAPIView):
    permission_classes = (IsAdminUser,)
    
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer


class CampaignDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAdminUser,)
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer


class CampaignCreate(generics.CreateAPIView):
    permission_classes = (IsAdminUser,)
    queryset = Campaign.objects.all()
    serializer_class = CampaignCreateSerializer
