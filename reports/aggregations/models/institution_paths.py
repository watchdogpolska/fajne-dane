from dataclasses import field, dataclass
from functools import cache
from typing import List, Dict

from campaigns.models import InstitutionGroup


InstitutionGroupPath = List[InstitutionGroup]


@dataclass
class InstitutionGroupPaths:
    _paths: List[InstitutionGroupPath] = field(default_factory=list)
    _mapping: Dict[int, InstitutionGroup] = field(default_factory=dict)
    _max_length: int = field(init=False, default=None)

    def add_path(self, path: InstitutionGroupPath):
        self._paths.append(path)
        for institution in path:
            if institution not in self._mapping:
               self._mapping[institution.id] = institution
        self._max_length = max(map(len, self._paths))

    @property
    def paths(self) -> List[InstitutionGroupPath]:
        return self.paths

    @property
    def max_length(self) -> int:
        return self._max_length

    @property
    def mapping(self) -> Dict[int, InstitutionGroup]:
        return self._mapping


def get_group_path(group: InstitutionGroup) -> List[InstitutionGroup]:
    _group = group
    _path = []
    while _group:
        _path.append(_group)
        _group = _group.parent
    return _path


def create_institution_group_paths(groups_ids: List[int]) -> InstitutionGroupPaths:
    paths = InstitutionGroupPaths()
    groups = InstitutionGroup.objects.filter(id__in=groups_ids)
    for group in groups:
        paths.add_path(get_group_path(group))
    return paths
