from reports.api.views.components.base import BaseDataComponentCreate
from reports.serializers.components.map_frequency import MapFrequencyComponentSerializer


class FrequencyMapComponentCreate(BaseDataComponentCreate):
    serializer_class = MapFrequencyComponentSerializer
