from django.core.exceptions import ValidationError
from django.test import TestCase

from campaigns.models import InstitutionGroup, Institution
from campaigns.models.dto import InstitutionDTO
from campaigns.models.factory import InstitutionsFactory
from tests.campaigns.conftest import basic_institution_group


class InstitutionFactoryTestCase(TestCase):

    def test_create(self):
        """Tests creating a campaign with a correct template."""
        factory = InstitutionsFactory(basic_institution_group())
        institution = factory.create(InstitutionDTO(key="1", name="test"))
        self.assertIsInstance(institution, Institution)
        self.assertEqual(institution.key, "1")
        self.assertEqual(institution.name, "test")

    def test_bulk_create(self):
        """Tests creating a campaign with a correct template."""
        factory = InstitutionsFactory(basic_institution_group())

        dtos = [
            InstitutionDTO(key="1", name="test1"),
            InstitutionDTO(key="2", name="test2", metadata={"field": "value"})
        ]
        institutions = factory.bulk_create(dtos)
        self.assertEqual(len(institutions), 2)

        for obj, dto in zip(institutions, dtos):
            self.assertEqual(obj.key, dto.key)
            self.assertEqual(obj.name, dto.name)
