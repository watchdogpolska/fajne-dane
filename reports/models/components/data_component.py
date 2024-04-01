from django.db import models

from .component import ReportComponent


class DataComponent(ReportComponent):
    data_view = models.ForeignKey("DataView",
                                  on_delete=models.CASCADE,
                                  related_name="report_components")
