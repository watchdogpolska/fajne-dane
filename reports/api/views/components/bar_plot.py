from reports.api.views.components.base import BaseDataComponentCreate
from reports.serializers.components.bar_plot import BarPlotComponentSerializer


class BarPlotComponentCreate(BaseDataComponentCreate):
    serializer_class = BarPlotComponentSerializer
