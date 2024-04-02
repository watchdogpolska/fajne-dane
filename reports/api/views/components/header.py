from reports.api.views.components.base import BaseComponentCreate
from reports.serializers.components.header import HeaderComponentSerializer


class HeaderComponentCreate(BaseComponentCreate):
    serializer_class = HeaderComponentSerializer
