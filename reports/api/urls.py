from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from .views import (
    ReportRender,
    ReportList,
    ReportDetails,
    DataSourceList,
    DataSourceDetails,
    HTMLComponentCreate,
    HeaderComponentCreate,
    BarPlotComponentCreate,
    ReportComponentDetails,
)


urlpatterns = [
    path('', ReportList.as_view(), name="reports_list"),
    path('<int:pk>/', ReportDetails.as_view(), name="report_details"),
    path('<int:pk>/render/', ReportRender.as_view(), name="report_render"),
    path('<int:report_id>/components/create/html/', HTMLComponentCreate.as_view(), name="html_component_create"),
    path('<int:report_id>/components/create/header/', HeaderComponentCreate.as_view(), name="header_component_create"),
    path(
        '<int:report_id>/components/create/barplot/',
        BarPlotComponentCreate.as_view(),
        name="barplot_component_create"
    ),
    path('components/<int:pk>/', ReportComponentDetails.as_view(), name="report_component_details"),
    path('sources/', DataSourceList.as_view(), name="data_source_list"),
    path('sources/<int:pk>/', DataSourceDetails.as_view(), name="data_source_details"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
