from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

from campaigns.models import Document, Campaign, Source
from tests.unit.campaigns.conftest import basic_campaign_template


class DocumentTestCase(TestCase):
    def setUp(self):
        Campaign.objects.create(
            name="test1",
            template=basic_campaign_template()
        )
        Source.objects.create(name="test")

    def test_creating_with_no_campaign(self):
        with self.assertRaises(ValidationError):
            Document.objects.create()

    def test_creating_with_no_source(self):
        with self.assertRaises(ValidationError):
            Document.objects.create(
                campaign=Campaign.objects.first(),
                data={"institution_id": 1}
            )

    def test_creating(self):
        document = Document.objects.create(
            campaign=Campaign.objects.first(),
            source=Source.objects.first(),
            data={"institution_id": 1}
        )
        self.assertIsInstance(document, Document)

    def test_incorrect_data(self):
        with self.assertRaises(ValidationError) as e:
            Document.objects.create(
                campaign=Campaign.objects.first(),
                source=Source.objects.first(),
                data={"project_id": 1}
            )
        exceptions = e.exception.error_dict['__all__']
        self.assertEqual(exceptions[0].code, "missing-field")
