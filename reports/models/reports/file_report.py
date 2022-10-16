from io import BytesIO

import pandas as pd

from django.core.files.base import ContentFile
from django.db import models

from reports.generators import FileReportBuilder
from .report import Report


class FileReport(Report):
    data_source = models.ForeignKey("CampaignDataSource",
                                    on_delete=models.CASCADE,
                                    related_name="file_reports")
    file = models.FileField(upload_to='file_reports')

    def _generate(self):
        builder = FileReportBuilder(self)
        df = builder.generate()

        output = BytesIO()
        writer = pd.ExcelWriter(output, engine='xlsxwriter')
        df.to_excel(writer)
        writer.save()

        output_file = ContentFile(output.getvalue())
        self.file.save(f"{self.name}.xlsx", output_file)
