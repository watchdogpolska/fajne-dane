from django.db import models

from .component import ReportComponent


class DataComponent(ReportComponent):
    data_view = models.ForeignKey("DataView",
                                  on_delete=models.CASCADE,
                                  related_name="report_components")

    @property
    def data_url(self) -> str:
        if self.data_view:
            return self.data_view.file.url
