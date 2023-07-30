from rest_framework import generics
from rest_framework.permissions import IsAdminUser, AllowAny

from campaigns.serializers import (
    CampaignSerializer, CampaignCreateSerializer, CampaignFullSerializer
)
from campaigns.models import Campaign


class CampaignList(generics.ListAPIView):
    permission_classes = (AllowAny,)
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer


class CampaignDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAdminUser,)
    queryset = Campaign.objects.all()
    serializer_class = CampaignFullSerializer


class CampaignCreate(generics.CreateAPIView):
    permission_classes = (IsAdminUser,)
    queryset = Campaign.objects.all()
    serializer_class = CampaignCreateSerializer
