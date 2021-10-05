from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import (
    CampaignList, CampaignDetail, CampaignCreate,
    DocumentList, DocumentDetail,
    QueryList, QueryDetail,
    RecordList, RecordDetail
)

urlpatterns = [
    path('campaigns/', CampaignList.as_view()),
    path('campaigns/create/', CampaignCreate.as_view()),
    path('campaigns/<int:pk>/', CampaignDetail.as_view()),
    path('documents/', DocumentList.as_view()),
    path('documents/<int:pk>/', DocumentDetail.as_view()),
    path('queries/', QueryList.as_view()),
    path('queries/<int:pk>/', QueryDetail.as_view()),
    path('records/', RecordList.as_view()),
    path('records/<int:pk>/', RecordDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
