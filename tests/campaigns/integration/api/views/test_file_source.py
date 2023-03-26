from django.test import TestCase, Client
from unittest import skip
from django.utils.datetime_safe import datetime

from campaigns.models import FileSource
from tests.campaigns.conftest import basic_campaign, basic_campaign_with_documents, advanced_campaign_with_documents, \
    basic_campaign_with_queries, advanced_campaign_with_queries, setup_institutions
from tests.conftest import user1, basic_campaign_documents_file, wrong_advanced_campaign_documents_file
from tests.utils import serialize_date


class FileSourceListTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_file_source_list(self):
        user = user1(is_active=True, is_staff=True)
        self.client.force_login(user)

        advanced_campaign_with_documents()  # other campaign
        campaign = basic_campaign_with_documents()

        response = self.client.get(
            f"/api/v1/campaigns/{campaign.id}/sources/"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(FileSource.objects.count(), 2)
        self.assertEqual(campaign.file_sources.count(), 1)
        self.assertEqual(len(response.data), 1)

        source = campaign.file_sources.first()
        self.assertEqual(response.data[0], {
            "id": source.id,
            'name': source.name,
            'description': source.description,
            'source_link': source.source_link,
            "source_date": serialize_date(source.source_date),
            "created": serialize_date(source.created),
            'file': None,
            'type': source.type
        })


class FileSourceDetailTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_file_source_get(self):
        user = user1(is_active=True, is_staff=True)
        self.client.force_login(user)

        campaign = basic_campaign_with_documents()
        source = campaign.file_sources.first()

        response = self.client.get(
            f"/api/v1/campaigns/{campaign.id}/sources/{source.id}/"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {
            "id": source.id,
            'name': source.name,
            'description': source.description,
            "source_link": source.source_link,
            "source_date": serialize_date(source.source_date),
            "created": serialize_date(source.created),
            'file': None,
            'type': source.type
        })

    def test_file_source_patch(self):
        user = user1(is_active=True, is_staff=True)
        self.client.force_login(user)

        campaign = basic_campaign_with_documents()
        source = campaign.file_sources.first()

        response = self.client.patch(
            f"/api/v1/campaigns/{campaign.id}/sources/{source.id}/",
            data={
                'description': "other"
            },
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)

        source.refresh_from_db()
        self.assertEqual(source.description, "other")

    def test_file_source_delete(self):
        user = user1(is_active=True, is_staff=True)
        self.client.force_login(user)

        campaign = basic_campaign_with_documents()
        source = campaign.file_sources.first()

        response = self.client.delete(
            f"/api/v1/campaigns/{campaign.id}/sources/{source.id}/",
        )
        self.assertEqual(response.status_code, 204)
        self.assertIsNone(FileSource.objects.filter(id=source.id).first())
        self.assertEqual(campaign.file_sources.count(), 0)
        self.assertEqual(campaign.documents.count(), 0)


class FileSourceCreateTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    @skip("This logic should be rewritten in a form of a worker")
    def test_file_source_create(self):
        user = user1(is_active=True, is_staff=True)
        self.client.force_login(user)

        setup_institutions()
        campaign = basic_campaign_with_queries()
        with basic_campaign_documents_file() as fp:
            response = self.client.post(
                f"/api/v1/campaigns/{campaign.id}/sources/create/",
                data={
                    "name": "file1",
                    "description": "description",
                    'source_link': 'http://source.link',
                    'source_date': serialize_date(datetime(2021, 12, 24)),
                    "file": fp
                }
            )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, {
            'is_valid': True,
            'file_errors': [],
            'documents_errors': [],
            'valid_documents_count': 4,
            'invalid_documents_count': 0
        })
        self.assertEqual(campaign.documents.count(), 4)

    def test_file_source_create_wrong(self):
        user = user1(is_active=True, is_staff=True)
        self.client.force_login(user)

        campaign = advanced_campaign_with_queries()
        with wrong_advanced_campaign_documents_file() as fp:
            response = self.client.post(
                f"/api/v1/campaigns/{campaign.id}/sources/create/",
                data={
                    "name": "file1",
                    "description": "description",
                    'source_link': 'http://source.link',
                    'source_date': serialize_date(datetime(2021, 12, 24)),
                    "file": fp
                }
            )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['is_valid'], False)
        self.assertEqual(response.data['valid_documents_count'], 1)
        self.assertEqual(response.data['invalid_documents_count'], 3)
        self.assertEqual(len(response.data['documents_errors']), 3)
        self.assertEqual(len(response.data['file_errors']), 0)

    def test_file_source_create_no_permission(self):
        user = user1(is_active=True, is_staff=False)
        self.client.force_login(user)

        campaign = basic_campaign_with_queries()
        with basic_campaign_documents_file() as fp:
            response = self.client.post(
                f"/api/v1/campaigns/{campaign.id}/sources/create/",
                data={
                    "name": "file1",
                    "description": "description",
                    'source_link': 'http://source.link',
                    'source_date': serialize_date(datetime(2021, 12, 24)),
                    "file": fp
                }
            )
        self.assertEqual(response.status_code, 403)


class FileSourceValidateTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_file_source_validate(self):
        user = user1(is_active=True, is_staff=True)
        self.client.force_login(user)

        campaign = basic_campaign_with_queries()
        with basic_campaign_documents_file() as fp:
            response = self.client.post(
                f"/api/v1/campaigns/{campaign.id}/sources/validate/",
                data={
                    "file": fp
                }
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {
            'is_valid': True,
            'file_errors': [],
            'documents_errors': [],
            'valid_documents_count': 4,
            'invalid_documents_count': 0
        })

    def test_file_source_validate_invalid(self):
        user = user1(is_active=True, is_staff=True)
        self.client.force_login(user)

        campaign = advanced_campaign_with_queries()
        with wrong_advanced_campaign_documents_file() as fp:
            response = self.client.post(
                f"/api/v1/campaigns/{campaign.id}/sources/validate/",
                data={
                    "file": fp
                }
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['is_valid'], False)
        self.assertEqual(response.data['valid_documents_count'], 1)
        self.assertEqual(response.data['invalid_documents_count'], 3)
