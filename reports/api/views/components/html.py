from reports.api.views.components.base import BaseComponentCreate
from reports.serializers.components.html import HTMLComponentSerializer


class HTMLComponentCreate(BaseComponentCreate):
    serializer_class = HTMLComponentSerializer
