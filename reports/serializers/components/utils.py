from typing import Type

from rest_framework import serializers

from reports.models.components import ReportComponent, ReportComponentTypes
from .bar_plot import BarPlotComponentSerializer
from .header import HeaderComponentSerializer
from .html import HTMLComponentSerializer
from .map_frequency import MapFrequencyComponentSerializer
from .table import TableComponentSerializer


class ReportComponentTypeNotFound(Exception):
    ...


def get_report_component_serializer(source_type: ReportComponent) -> Type[serializers.Serializer]:
    if source_type == ReportComponentTypes.TABLE:
        return TableComponentSerializer
    elif source_type == ReportComponentTypes.BAR_PLOT:
        return BarPlotComponentSerializer
    elif source_type == ReportComponentTypes.HTML:
        return HTMLComponentSerializer
    elif source_type == ReportComponentTypes.HEADER:
        return HeaderComponentSerializer
    elif source_type == ReportComponentTypes.MAP_FREQUENCY:
        return MapFrequencyComponentSerializer
    raise ReportComponentTypeNotFound(f"Type unknown: {source_type}")
