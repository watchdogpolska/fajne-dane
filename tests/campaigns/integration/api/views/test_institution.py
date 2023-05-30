from django.test import TestCase, Client

from campaigns.models import Institution
from tests.campaigns.conftest import basic_institution_group, basic_institution, basic_document, child_institution
from tests.conftest import user1


class InstitutionListTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_institutions_list(self):
        institution = child_institution()
        institutions_group = institution.group

        user = user1(is_active=True, is_staff=True)
        self.client.force_login(user)

        response = self.client.get(f"/api/v1/campaigns/institution-groups/{institutions_group.id}/institutions/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), institutions_group.institutions.count())

        for institution_data in response.data:
            if institution_data['id'] != institution.id: continue

            self.assertEqual(institution_data, {
                'id': institution.id,
                "parent": {
                    "id": institution.parent.id,
                    "key": institution.parent.key,
                    "name": institution.parent.name
                },
                'key': institution.key,
                'name': institution.name,
                'link': institution.link,
            })
    def test_institutions_list_search(self):
        institution = child_institution()
        institutions_group = institution.group

        user = user1(is_active=True, is_staff=True)
        self.client.force_login(user)

        response = self.client.get(
            f"/api/v1/campaigns/institution-groups/{institutions_group.id}/institutions/?search=2")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

        self.assertEqual(response.data[0], {
                'id': institution.id,
                "parent": {
                    "id": institution.parent.id,
                    "key": institution.parent.key,
                    "name": institution.parent.name
                },
                'key': institution.key,
                'name': institution.name,
                'link': institution.link,
            })

    def test_institution_create(self):
        institutions_group = basic_institution_group()

        user = user1(is_active=True, is_staff=True)
        self.client.force_login(user)

        self.assertEqual(Institution.objects.count(), 0)

        response = self.client.post(
                f"/api/v1/campaigns/institution-groups/{institutions_group.id}/institutions/create/",
            data={
                "key": "234234",
                "name": "institution name",
                "link": "http://url.pl"
            }
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Institution.objects.count(), 1)

        institution = Institution.objects.first()
        self.assertEqual(response.data, {
            'id': institution.id,
            "group_id": institution.group_id,
            "parent_id": institution.parent_id,
            "key": institution.key,
            "name": institution.name,
            "link": institution.link,
            "address": institution.address,
        })


class InstitutionGroupDetailsTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_institution_details(self):
        institution = basic_institution()

        user = user1(is_active=True, is_staff=True)
        self.client.force_login(user)

        response = self.client.get(
            f"/api/v1/campaigns/institution/{institution.id}/"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {
            'id': institution.id,
            "group_id": institution.group_id,
            "key": institution.key,
            "name": institution.name,
            "link": institution.link,
            "address": institution.address,
        })

    def test_institution_patch(self):
        institution = basic_institution()

        user = user1(is_active=True, is_staff=True)
        self.client.force_login(user)

        self.assertIsNone(institution.address)

        response = self.client.patch(
            f"/api/v1/campaigns/institution/{institution.id}/",
            data={"address": "test address"},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)

        institution.refresh_from_db()
        self.assertEqual(institution.address, "test address")

    def test_institution_delete_empty(self):
        institution = basic_institution()

        user = user1(is_active=True, is_staff=True)
        self.client.force_login(user)

        response = self.client.delete(f"/api/v1/campaigns/institution/{institution.id}/")
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Institution.objects.count(), 0)

    def test_institution_group_delete_conflict(self):
        _document = basic_document()
        institution = _document.institution

        user = user1(is_active=True, is_staff=True)
        self.client.force_login(user)

        response = self.client.delete(f"/api/v1/campaigns/institution/{institution.id}/")
        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.data['detail'].code, "institution_has_documents")
