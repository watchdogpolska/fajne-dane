from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from .views import (
    CampaignList, CampaignDetail, CampaignCreate,
    DocumentList, DocumentDetail, DocumentCreate,
    QueryList, QueryDetail,
    RecordList, RecordCreate, RecordDetail,
    FileSourceList, FileSourceCreate, FileSourceDetail, FileSourceValidate,
    GetMetaTemplate, ValidateCampaignTemplate,
    DocumentQueryDetail, DocumentQueryStatusList
)


urlpatterns = [
    path('', CampaignList.as_view(), name="campaigns_list"),
    path('create/', CampaignCreate.as_view(), name="campaign_create"),
    path('template/', GetMetaTemplate.as_view(), name="get_meta_template"),
    path('template/validate/', ValidateCampaignTemplate.as_view(), name="validate_campaign_template"),
    path('<int:pk>/', CampaignDetail.as_view(), name="campaign_details"),
    path('<int:campaign_id>/sources/', FileSourceList.as_view(), name="file_sources_list"),
    path('<int:campaign_id>/sources/validate/', FileSourceValidate.as_view(), name="file_source_validate"),
    path('<int:campaign_id>/sources/create/', FileSourceCreate.as_view(), name="file_source_create"),
    path('<int:campaign_id>/sources/<int:pk>/', FileSourceDetail.as_view(), name="file_source_detail"),
    path('<int:campaign_id>/documents/', DocumentList.as_view(), name="campaigns_documents_list"),
    path('<int:campaign_id>/documents/create/', DocumentCreate.as_view(), name="document_create"),
    path('documents/<int:pk>/', DocumentDetail.as_view(), name="documents_details"),
    path('documents/<int:pk>/statuses/', DocumentQueryStatusList.as_view(), name="document_query_status_list"),
    path('<int:campaign_id>/queries/', QueryList.as_view(), name="campaign_queries_list"),
    path('queries/<int:pk>/', QueryDetail.as_view(), name="query_details"),
    path('records/<int:pk>/', RecordDetail.as_view(), name="record_details"),
    path('doc-queries/<int:pk>/', DocumentQueryDetail.as_view(), name="document_query_details"),
    path('doc-queries/<int:doc_query_id>/records/', RecordList.as_view(), name="record_list"),
    path('doc-queries/<int:doc_query_id>/records/create/', RecordCreate.as_view(), name="record_create"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
