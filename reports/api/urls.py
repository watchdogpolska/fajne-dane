from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from .views.reports import ReportRender, ReportList

urlpatterns = [
    path('', ReportList.as_view(), name="reports_list"),
    path('<int:pk>/', ReportRender.as_view(), name="report_render"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
