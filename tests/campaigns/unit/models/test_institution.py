from django.test import TestCase

from campaigns.models.institutions import Institution, InstitutionGroup, InstitutionTypes


def basic_institution_group() -> InstitutionGroup:
    return InstitutionGroup.objects.create(
        name="test_group",
        type=InstitutionTypes.ORGANIZATION
    )


class InstitutionGroupTestCase(TestCase):
    def test_creating(self):
        group, _ = InstitutionGroup.objects.get_or_create(
            name="test1",
            type=InstitutionTypes.ORGANIZATION
        )
        self.assertIsInstance(group, InstitutionGroup)


class InstitutionTestCase(TestCase):
    def test_creating(self):
        institution, _ = Institution.objects.get_or_create(
            name="test1",
            group=basic_institution_group()
        )
        self.assertIsInstance(institution, Institution)
