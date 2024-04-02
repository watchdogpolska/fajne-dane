from reports.api.views.components.base import BaseComponentCreate
from reports.serializers.components.references import ReferencesComponentSerializer


class ReferencesComponentCreate(BaseComponentCreate):
    serializer_class = ReferencesComponentSerializer
