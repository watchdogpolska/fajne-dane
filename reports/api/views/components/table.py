from reports.api.views.components.base import BaseDataComponentCreate
from reports.serializers.components.table import TableComponentSerializer


class TableComponentCreate(BaseDataComponentCreate):
    serializer_class = TableComponentSerializer
