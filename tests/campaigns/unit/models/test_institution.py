from django.test import TestCase

from campaigns.models.institutions import Institution, InstitutionGroup
from tests.campaigns.conftest import basic_institution_group


class InstitutionGroupTestCase(TestCase):
    def test_creating(self):
        group, _ = InstitutionGroup.objects.get_or_create(
            name="test1",
        )
        self.assertIsInstance(group, InstitutionGroup)


class InstitutionTestCase(TestCase):
    def test_creating(self):
        institution, _ = Institution.objects.get_or_create(
            name="test1",
            group=basic_institution_group()
        )
        self.assertIsInstance(institution, Institution)
