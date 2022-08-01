from typing import Type

from rest_framework import serializers

from campaigns.models.institutions import InstitutionTypes


def get_institution_serializer(institution_type: InstitutionTypes) -> Type[serializers.Serializer]:
    if institution_type == InstitutionTypes.ORGANIZATION:
        return
    raise Exception("Type unknown")
