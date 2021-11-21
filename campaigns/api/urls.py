from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from .views import (
    CampaignList, CampaignDetail, CampaignCreate,
    DocumentList, DocumentDetail, DocumentCreate,
    QueryList, QueryDetail,
    RecordList, RecordDetail, RecordCreate,
    FileSourceList, FileSourceCreate, FileSourceDetail
)


urlpatterns = [
    path('', CampaignList.as_view(), name="campaigns_list"),
    path('create/', CampaignCreate.as_view(), name="campaign_create"),
    path('<int:pk>/', CampaignDetail.as_view(), name="campaign_details"),
    path('<int:campaign_id>/sources/', FileSourceList.as_view(), name="file_sources_list"),
    path('<int:campaign_id>/sources/create/', FileSourceCreate.as_view(), name="file_source_create"),
    path('<int:campaign_id>/sources/<int:pk>/', FileSourceDetail.as_view(), name="file_source_detail"),
    path('<int:campaign_id>/documents/', DocumentList.as_view(), name="campaigns_documents_list"),
    path('<int:campaign_id>/documents/create/', DocumentCreate.as_view(), name="document_create"),
    path('documents/<int:pk>/', DocumentDetail.as_view(), name="documents_details"),
    path('<int:campaign_id>/queries/', QueryList.as_view(), name="campaign_queries_list"),
    path('queries/<int:pk>/', QueryDetail.as_view(), name="query_details"),
    path('documents/<int:document_id>/records/', RecordList.as_view(), name="documents_records_list"),
    path('documents/<int:document_id>/records/create/', RecordCreate.as_view(), name="record_create"),
    path('records/<int:pk>/', RecordDetail.as_view(), name="record_details"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
