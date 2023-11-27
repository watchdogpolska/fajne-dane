from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from .views import ReportRender, ReportList, ReportDetails, DataSourceList


urlpatterns = [
    path('', ReportList.as_view(), name="reports_list"),
    path('<int:pk>/', ReportDetails.as_view(), name="report_details"),
    path('<int:pk>/render', ReportRender.as_view(), name="report_render"),
    path('sources/', DataSourceList.as_view(), name="data_source_list"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
