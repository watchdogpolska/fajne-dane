from django.core.files.base import ContentFile
from django.db import models

from reports.generators import FileReportBuilder
from .report import Report
from ...renderers.campaign_file_report.renderer import CampaignFileReportRenderer


class FileReport(Report):
    data_source = models.ForeignKey("DataSource",
                                    on_delete=models.CASCADE,
                                    related_name="file_reports")
    file = models.FileField(upload_to='file_reports')

    def _generate(self):
        builder = FileReportBuilder(self)
        renderer = CampaignFileReportRenderer(builder.generate())
        output = renderer.render()
        output_file = ContentFile(output.getvalue())
        self.file.save(f"{self.name}.xlsx", output_file)
