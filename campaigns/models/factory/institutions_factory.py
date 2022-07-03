from dataclasses import dataclass
from typing import List

from django.db import transaction

from campaigns.models import InstitutionGroup, Institution
from campaigns.models.dto.institution import InstitutionDTO
from fajne_dane.core.base.factory import BaseFactory


@dataclass
class InstitutionsFactory(BaseFactory):
    group: InstitutionGroup

    @transaction.atomic
    def create(self, institution_dto: InstitutionDTO) -> Institution:
        return Institution.objects.create(
            key=institution_dto.key,
            name=institution_dto.name,
            group=self.group
        )

    @transaction.atomic
    def bulk_create(self, institution_dtos: List[InstitutionDTO]) -> List[Institution]:
        _institutions = [
            Institution(key=dto.key, name=dto.name,group=self.group)
            for dto in institution_dtos
        ]
        institutions = Institution.objects.bulk_create(_institutions)
        return institutions
