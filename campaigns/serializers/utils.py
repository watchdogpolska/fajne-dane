from typing import Type

from rest_framework import serializers

from campaigns.models.sources.source import SourceTypes
from campaigns.serializers.sources import UserSourceSerializer, FileSourceSerializer


def get_source_serializer(source_type: SourceTypes) -> Type[serializers.Serializer]:
    if source_type == SourceTypes.USER:
        return UserSourceSerializer
    elif source_type == SourceTypes.FILE:
        return FileSourceSerializer
    raise Exception("Type unknown")
