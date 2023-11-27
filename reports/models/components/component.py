from django.db import models

from .consts import ReportComponentTypes


class ReportComponent(models.Model):
    report = models.ForeignKey("Report",
                               on_delete=models.CASCADE,
                               related_name="components")

    name = models.CharField(max_length=30)
    type = models.CharField(max_length=30,
                            choices=ReportComponentTypes.choices,
                            default=ReportComponentTypes.TABLE)

    class Meta:
        unique_together = ('name', 'report',)

    def to_child(self) -> "ReportComponent":
        """
        Used to get an object of a child type object.
        """
        import reports.models.components as c
        if self.type == ReportComponentTypes.TABLE:
            return c.table.TableComponent.objects.get(id=self.id)
        if self.type == ReportComponentTypes.BAR_PLOT:
            return c.bar_plot.BarPlotComponent.objects.get(id=self.id)
        if self.type == ReportComponentTypes.MAP_FREQUENCY:
            return c.map_frequency.MapFrequencyComponent.objects.get(id=self.id)
        if self.type == ReportComponentTypes.HTML:
            return c.html.HTMLComponent.objects.get(id=self.id)
        if self.type == ReportComponentTypes.HEADER:
            return c.header.HeaderComponent.objects.get(id=self.id)
        raise TypeError(f"No child mapping found for type: {self.type}")
