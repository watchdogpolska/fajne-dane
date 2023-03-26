from django.test import TestCase, Client

from campaigns.models import InstitutionGroup
from tests.campaigns.conftest import setup_institutions, basic_institution_group, basic_document
from tests.conftest import user1


class InstitutionGroupListTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_institution_group_list(self):
        _institutions = setup_institutions()
        institution_group = _institutions[0].group

        user = user1(is_active=True, is_staff=True)
        self.client.force_login(user)

        response = self.client.get("/api/v1/campaigns/institution-groups/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0], {
            "id": institution_group.id,
            "parent_id": institution_group.parent_id,
            "name": institution_group.name,
            "institutions_count": institution_group.institutions.count()
        })

    def test_institution_group_create_default_fields(self):
        user = user1(is_active=True, is_staff=True)
        self.client.force_login(user)

        self.assertEqual(InstitutionGroup.objects.count(), 0)

        response = self.client.post(
            "/api/v1/campaigns/institution-groups/create/",
            data={
                "name": "group name",
            }
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(InstitutionGroup.objects.count(), 1)

        institution_group = InstitutionGroup.objects.first()
        self.assertEqual(response.data, {
            "id": institution_group.id,
            "parent_id": institution_group.parent_id,
            "name": "group name",
            "fields": ["link"]
        })

    def test_institution_group_create_fields(self):
        user = user1(is_active=True, is_staff=True)
        self.client.force_login(user)

        self.assertEqual(InstitutionGroup.objects.count(), 0)

        response = self.client.post(
            "/api/v1/campaigns/institution-groups/create/",
            data={
                "name": "group name",
                "fields": ["address"]
            }
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(InstitutionGroup.objects.count(), 1)

        institution_group = InstitutionGroup.objects.first()
        self.assertEqual(response.data, {
            'id': institution_group.id,
            "parent_id": institution_group.parent_id,
            'name': 'group name',
            "fields": ["address"]
        })


class InstitutionGroupDetailsTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_institution_group_details(self):
        _institutions = setup_institutions()
        institutions_group = _institutions[0].group

        user = user1(is_active=True, is_staff=True)
        self.client.force_login(user)

        response = self.client.get(
            f"/api/v1/campaigns/institution-groups/{institutions_group.id}/"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {
            "id": institutions_group.id,
            "name": institutions_group.name,
            "institutions_count": institutions_group.institutions.count(),
            "fields": institutions_group.fields
        })

    def test_institution_group_patch(self):
        institutions_group = basic_institution_group()

        user = user1(is_active=True, is_staff=True)
        self.client.force_login(user)

        self.assertEqual(institutions_group.fields, ["link"])

        response = self.client.patch(
            f"/api/v1/campaigns/institution-groups/{institutions_group.id}/",
            data={"fields": ["address"]},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)

        institutions_group.refresh_from_db()
        self.assertEqual(institutions_group.fields, ["address"])

    def test_institution_group_delete_empty(self):
        institutions_group = basic_institution_group()

        user = user1(is_active=True, is_staff=True)
        self.client.force_login(user)

        response = self.client.delete(f"/api/v1/campaigns/institution-groups/{institutions_group.id}/")
        self.assertEqual(response.status_code, 204)
        self.assertEqual(InstitutionGroup.objects.count(), 0)

    def test_institution_group_delete_conflict(self):
        _document = basic_document()
        institutions_group = _document.institution.group

        user = user1(is_active=True, is_staff=True)
        self.client.force_login(user)

        response = self.client.delete(f"/api/v1/campaigns/institution-groups/{institutions_group.id}/")
        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.data['detail'].code, "institution_groups_has_documents")
